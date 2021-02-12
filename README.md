# data17-finalproject
This project is designed to extract data about spartans and sparta applicants from S3,
clean it, and load it into a normalised SQL database.
The data can be visualised in an interactive dashboard, which shows summary statistics and single person views.

## Contents
1. Installation and setup
2. User guide
3. Contributors

## Installation
To install the pipeline, database and dashboard:
1. Install all programs/modules listed in the requirements file
2. Using git, pull the project code from https://github.com/AmyCatling/data17-finalproject/
3. Update credentials as needed in the file config.ini
4. Run the file fully_normalised.sql in Azure. This will create the database.
    1. The Entity Relationship Diagram is stored in the file fully_normalised_erd.drawio

## User guide
Once setup is complete, the pipeline code can be run by running main.py
The pipeline will run, transferring the data from S3 to SQL
Logging information for the pipeline is saved in log files
The dashboard can be initialised by running the file cl_app.py, then following the link in the output

### Dashboard guide
Description of dashboard goes here

## Contributors
Amy Catling  
Hannah Bouteba  
Hayder Morsel  
Joe Stallibrass  
Louis Goneta  
Lucio Bonforte  
Mat Syrek  
Ross Wiseman  
Thomas Woods  
William Hallam  

Special thanks to David Harvey, who provided the training and resources to allow the project to be completed
