import pandas as pd
import numpy as np
import json
from jsonschema import validate
import time
import logging
import os

impression_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "app_id": {"type": "number"},
        "country_code": {"type": ["string","null"]},
        "advertiser_id": {"type": "number"},
    },
    "required": ["id","app_id","advertiser_id","country_code"],
}

click_schema = {
    "type": "object",
    "properties": {
        "impression_id": {"type": "string"},
        "revenue": {"type": "number"},
    },
    "required": ["impression_id","revenue"],
}

impression_filepath="input"
clicks_filepath="input"

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def json_validate(json_obj,schema):
    try:
        validate(instance=json_obj,schema=schema)
        return True
    except Exception as e:
        logger.warning(e.__str__())
        return False

def json_parser(files_path,schema):
    data=[]
    for file in files_path:
        try:
            with open(file) as f:
                temp=json.load(f)
                for record in temp:
                    if json_validate(record, schema)==False:
                        temp.remove(record)
                data.extend(temp)
        except FileNotFoundError:
            logger.error("Error: File {} not found.".format(file))
        except PermissionError:
            logger.error("Error: Permission denied on reading {}.".format(file))
        except Exception as e:
            logger.error("Error: ",e.__str__())
    return pd.DataFrame(data)

def main():        
    ## part 1

    impression_files=input("Enter a list of impression file names seperated by commas: ")
    click_files=input("Enter a list of click file names seperated by commas: ")
    try:
        impression_files=impression_files.split(",")
        click_files=click_files.split(",")
    except Exception as e:
        logger.error(e.__str__())

    impression_fullPath = [os.path.join(impression_filepath,fPath) for fPath in impression_files]
    click_fullPath = [os.path.join(clicks_filepath,fPath) for fPath in click_files]

    impression_df=json_parser(impression_fullPath,impression_schema)
    clicks_df=json_parser(click_fullPath, click_schema)

    ## part 2

    impression_df[['id', 'country_code']] = impression_df[['id', 'country_code']].astype(str)
    impression_df[['app_id', 'advertiser_id']] = impression_df[['app_id', 'advertiser_id']].astype(int)
    impression_df=impression_df.drop_duplicates(subset=['app_id','country_code','id','advertiser_id'])

    clicks_df=clicks_df.drop_duplicates(subset=['impression_id','revenue'])

    complete_df=pd.merge(impression_df,clicks_df,left_on='id',right_on='impression_id',how="left")
    summary=complete_df.groupby(['app_id','country_code','advertiser_id']
                        ).agg({'id':'count','revenue':['count','sum']}).reset_index()
    summary.columns=['app_id','country_code','advertiser_id','impressions','clicks','revenue']
    report_section2=summary.groupby(['app_id','country_code']
                        ).agg({'impressions':'sum','clicks':'sum','revenue':'sum'}).reset_index()

    timestr = time.strftime("%Y%m%d%H%M%S")
    filename_path_section2='output/section2_'+timestr+'.json'
    report_section2.to_json(filename_path_section2,orient="records",indent=4)

    ## part 3

    summary['rate']=summary['revenue']/summary['impressions']
    top_five=summary.groupby(['app_id','country_code']).apply(lambda x: x.nlargest(5,columns=['rate'])).reset_index(drop=True)
    top_five=top_five[['app_id','country_code','advertiser_id']]
    top_five=top_five.groupby(['app_id','country_code'])['advertiser_id'].apply(list).reset_index()
    filename_path_section3='output/section3_'+timestr+'.json'
    top_five.to_json(filename_path_section3,orient="records",indent=4)

if __name__ == "__main__":
    main()