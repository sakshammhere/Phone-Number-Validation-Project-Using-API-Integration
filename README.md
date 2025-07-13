# Phone-Number-Validation-Project-Using-API-Integration
--> Introduction
This Project is built in python which uses VeriPhone API to validate phone numbers individually or as a CSV file. It checks the validity, carrier, country, and line type of each number and logs the results accordingly.
Application Programming Interfaces(API): The connection between 2 or more applications via their APIs, so that they can exchange data.(usually in JSON or XML). This includes push which means sending data to the API, while pull means receiving or pulling data from the API.

--> Features 
-Validates Phone numbers with proper Formatting check which includes : Only Integer Input, Length of the number to be 10 digits, Should always start with + followed by country code, Validates and verify Records from an uploaded CSV file in bulk wherein Ph_num should be the column name of the Mobile Number's list, Automatically skips duplicate mobile numbers which saves API calls and saves cost, Uses a tkinter based GUI for CSV file upload.

--> Libraries Used : requests(downloaded using pip), os, csv, datetime, tkinter

-->CSV Format for BULK Mode : 
-Sample :  Ph_num
          +14155552671
          +919876543210
          +447911123456

-->API USED : https://api.veriphone.io/v2/verify
This API returns : -phone_valid, country, carrier, phone_type


Author : Saksham Gupta 
Contact : guptasaksham0301@gmail.com










  
