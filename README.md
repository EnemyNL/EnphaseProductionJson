# EnphaseProductionJson
Python script reading Enphase envoy and storing wNow production in MySQL

This python script connects (when configured properly) to your Enphase Envoy to read current production and store it in MYSQL. 

Input your data in line 12, 37, 38, 39, 49 and 57.
Please note at this stage the script doesnt set up your database. The database the script is based on is set up as follows:
Table name: Production
Column 1: name id, type int(255), NO Null, Key PRI, Default NULL, Extra auto_increment
Column 2: name currentDateTime, type datetime, NO null, Default NULL
Column 3: name wnow, type float, Null YES, Default NULL

Works for me with firmware D5.0.62
