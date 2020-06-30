# Parking Lot

The project provides real time service for parking lot.
The app provides the client the ability to give an image of a vehicle licence plate path and get a decision whether the vehicle is approved to enter the parking lot according to preset logic. 
furthermore, it provides the ability to give a directory path that contains multiple images and get results for all images in directory.
Last function of the app gives the client info about all rejected vehicles from last week.
 

#### REST APIs:

##### insert_batch_cars
POST localhost:5000/insert_batch_cars
payload: 
```
{
	"path": "~\\ParkingLot\\ImageInfoExtractor\\images"
}
```
RESPONSE:
in "decisions" dict,
key: licence plate content identified by an ocrspace.
value: Is the vehicle approved?

```
{
    
    "decisions": {
        "206 09 CORPS alamy stock photo EHNGHM www alamy com": false,
        "DIPLOMA T Cur M DTH0507 i 5 10": false,
        "DIPLOMAT DB 0789": false,
        "DIPLOMAT DCY0477 issued By And Property Of The UNITED STATES DEPARTMENT OF STATE s 00656": false,
        "DIPLOMAT I CM0076": false,
        "DIPLOMAT I DL0416 g And STATES OEPARWENT OF": false,
        "DIPLOMAT Issued By And Property Of The SEP UNITED STATES DEPARTMENT OF STATE 00": false,
        "EDUC8 r SUPPORT EDUCATION": true,
        "FLORIDA CORPS": false,
        "FLORIDA EAR MARINE CORPS": false,
        "FLORIDA ENDLESS SU": true,
        "FLORIDA MARINE CORPS 09001265": false,
        "FLORIDA SURFN SNDLESSSÜMMER": true,
        "FLORIDA TRANSPORTER": false,
        "FLORIOA GOOOOA TRANSPORTER": false,
        "JUN 7SUE187": false,
        "MARINE CORPS": false
    },
    "message": "OK"
}
```
##### insert_car

POST localhost:5000/insert_car

payload: 
```
{
	"path": "~\\ParkingLot\\ImageInfoExtractor\\images\\2014-Florida-Endless-Summer-License-Plate-Surfing-Ocean.jpg"
}
```
RESPONSE:
```
{
    "message": "Car is permitted"
}
```
##### get last week rejected vehicles: 

GET localhost:5000/get_last_week_rejected_vehicles (GET)

each vehicle has its own "denied_entries" that contains info about the image & timestamp, contains licence plate content, and message about the decision
RESPONSE
```
{
    "message": "OK",
    "vehicles": [
        {
            "denied_entries": [
                {
                    "source": "../ImageInfoExtractor/images/ends_with.jpg",
                    "timestamp": "Tue, 30 Jun 2020 12:42:31 GMT"
                }
            ],
            "licence_plate_content": "JUN 7SUE187",
            "rejection_reason": "The vehicle cannot enter the parking lot because its license plate's last two digits are: 85/86/87/88/89/00"
        },
        {
            "denied_entries": [
                {
                    "source": "../ImageInfoExtractor/images/florida_Gflorida-dealer-tags-transporter_1_1ae3fb97efea87be53b8b92bce9a9b23.jpg",
                    "timestamp": "Tue, 30 Jun 2020 12:43:54 GMT"
                },
                {
                    "source": "../ImageInfoExtractor/images//florida_Gflorida-dealer-tags-transporter_1_1ae3fb97efea87be53b8b92bce9a9b23.jpg",
                    "timestamp": "Tue, 30 Jun 2020 14:46:49 GMT"
                },
                {
                    "source": "C:UsersItayPycharmProjectsParkingLotImageInfoExtractorimages/florida_Gflorida-dealer-tags-transporter_1_1ae3fb97efea87be53b8b92bce9a9b23.jpg",
                    "timestamp": "Tue, 30 Jun 2020 19:26:04 GMT"
                }
            ],
            "licence_plate_content": "FLORIDA TRANSPORTER",
            "rejection_reason": "The vehicle cannot enter the parking lot because its license plate starts with the letter 'G', i.e the vehicle is a transporter"
        }
    ]
}
```

## Install
pip install -R requirements.txt

## Running The App

## 1. Creating The database
create local database and run the following scripts to create the tables:
run: sqlqueries/migrations/create_table_decisions.sql
run: sqlqueries/migrations/create_table_plates.sql

## 2. arguments for the database:
arguments for mysql.connector: host, user, password, port are defined in ClientModule.
if any of these arguments are different in your db change the arguments in the module
    
## 3. database tables
The database is implemented in MySQL and consists of the following tables:
1. decisions - contains info about each decision, and metadata about the image
2. plates - contains info about the licence plates such as: plate_type, plate_content
    
### 4. Run app
run: python Client/ClientModule.py
