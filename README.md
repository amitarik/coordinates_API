# API_GPS
A Rest API Using Python3.7 Flask framework.
The APi has 3 request
 
1. “/api/getAddresses” POST API. It is a HTTP POST method that enables to upload a
CSV file with point locations ( LAT/LON ) 
The file can be upload using Curl command or by the UI.
e.g. 
curl --location --request POST http://127.0.0.1:5000/api/getAddresses -F file=@"<Full .csv file>"

2. “/api/getResult/<id>” GET API . It is an API to retrieve a single stored results object
identified by “result_id” or "_id".
GET id : curl --location --request GET http://127.0.0.1:5000/api/getResult/<result_id>
GET id : curl --location --request GET http://127.0.0.1:5000/api/getResult/<_id>

3. “/api/getResult” GET API . It is an API to retrieve all results object
GET all: curl --location --request GET http://127.0.0.1:5000/api/getResult

The Object structs is as the following:
 {
“points”: [
{ “name” : “A”, “address” : “Some address...” },
{ “name” : “B”, “address” : “Some address...” },
{ “name” : “C”, “address” : “Some address...” },
],
“links”: [
{ “name” : “AB”, “distance” : 350.6 },
{ “name” : “BC”, “distance” : 125.8 },
{ “name” : “AC”, “distance” : 1024.9 }
"_id': b47d4112-31c2-4f02-a98d-10c3d6b001be
"result_id": 2
],
 

