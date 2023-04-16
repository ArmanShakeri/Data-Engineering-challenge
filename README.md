# Data-Engineering-challenge

This Python code is for Data Engineering challenge. Points to consider:
- The given impressions sample file has many duplicate records and my assumtion was that "id" column must be uniqe so I used distict and I droped duplicated records.
- Based on json schema some records are ignored and they are displayed on console as a warning when the code is executed.
- In the final result of section 2, clicks count of some aggregated records are greater than count of impressions and it is known that it doesn't seem logical, so I assumed there are some inconsistencies in the given sample file or I am not familiar with the logic behind it.
- The input files must be placed in the input directory.
- the result of the challenge will be placed in the output directory.

# Step to run

**Step 1**
install python3.10 and packages in requirement.txt

**Step 2**
place impression and click files in input directory.

**Step 3**
Change directory to project location and run this syntax:
``` 
python3.10 main.py

```
**Step 4**
Enter file names and seperate them with commas.
for example: file1.json,file2.json,file3.json
This code gets two lists of files: impressions and clicks.

**Step 5**
See the result in output directory. The report of section 2 is like section2_YYYYMMDDHHMISS.json and section 3 is like section3_YYYYMMDDHHMISS.json.