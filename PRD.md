#Product Requirements Document

--Instructions for Creating Script--

Step 1. 
Read the values in the file ./sample-data/Teema_Sample_Data.csv
Column headers are shown in row 1

Step 2. 
Create a new .copy of the file Parts_Template.csv in the /sample-data directory

Name this file Parts_TemplateN.csv where N will increment by 1 for each new template created.

Example output of a path to the new file: 
/sample-data/Parts_Template1.csv

Step 3. 
For each row in /sample-data/Parts_TemplateN.csv, copy the values from Teema_Sample_Data.csv and input that value into Parts_TemplateN.csv according to the following business logic:
1. If the value in Parts_TemplateN.csv
