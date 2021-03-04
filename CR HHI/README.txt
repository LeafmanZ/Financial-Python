AUTHOR: JIM ZIELEMAN
PROGRAM: INDUSTRY CONCENTRATION METRICS (CONCENTRATION RATIO & HHI)

Plots to browser and also saves as jpeg in the same working directory as the python program.

Dependencies:
pandas
easygui
plotly
psutil

Collecting Data Example:
https://wrds-web.wharton.upenn.edu/wrds//ds/compd/funda/index.cfm
Step 1
Date Variable: Data Date
Date Range: 2019-01 to 2019-12

Step 2
Search the entire database
Uncheck all the screening variables outputs

Step 3
Select: REVT, SIC
WHERE REVT IS NOT NULL AND SIC IS NOT NULL

Step 4
Output Format: .csv
