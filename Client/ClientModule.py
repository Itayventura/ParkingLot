import mysql.connector
from flask import jsonify, request, Flask
from future.backports.http.client import OK, NOT_FOUND
from EntryDecider.EntryDecider import EntryDecider
from Handlers.DecisionsHandler import DecisionsHandler
from Handlers.PlatesHandler import PlatesHandler
from Handlers.VehiclesHandler import VehiclesHandler
from ImageInfoExtractor.ImageInfoExtractor import ImageInfoExtractor
from Repository.Repository import Repository
import logging
import mysql.connector

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

cnx = mysql.connector.connect(host='localhost',
                              database='parking_lot',
                              user='root',
                              password='1234',
                              port='3306')
cursor = cnx.cursor()
logging.basicConfig(level=logging.INFO)
repository = Repository(cnx, cursor)
plates_handler = PlatesHandler(repository)
decisions_handler = DecisionsHandler(repository)
vehicles_handler = VehiclesHandler(repository)


class ClientModule:

    @staticmethod
    def get_last_week_declined_vehicles():
        """
        @:returns list of all vehicles not approved for entry last week
        """
        return vehicles_handler.select_vehicles()

    @staticmethod
    def print_report_last_week_declined_plates():
        """
        prints to logging info about all vehicles not approved for entry last week
        """
        logging.info("The following vehicles did not get permission of entering the parking lot:\n")
        vehicles = ClientModule.get_last_week_declined_vehicles()
        for vehicle in vehicles:
            logging.info(vehicle)

    @staticmethod
    def add_images_from_path(directory_path='../ImageInfoExtractor/images'):
        """
        @:param (str) directory path from which it iterates through all images, detects its plate content,
         makes a decision and writes it to local database.
        @:returns (dict) key(str): licence plate content. value(boolean): is permitted to enter?
        """
        licencePlateContent_imagePath_dict = ImageInfoExtractor.parse_images_text_from_dir_path(directory_path)
        if licencePlateContent_imagePath_dict is None:
            return None

        licencePlateContents = list(licencePlateContent_imagePath_dict.keys())
        plates = EntryDecider.get_plates(licencePlateContents)

        if licencePlateContent_imagePath_dict:
            plates_handler.insert_plates(plates)
            licencePlateContent_plateSqlID_dict = plates_handler.select_plates(licencePlateContents)
            imagePath_plateSqlID_dict = ClientModule.get_imagePath_plateSqlID_dict(licencePlateContent_plateSqlID_dict,
                                                                                   licencePlateContent_imagePath_dict)
            imagePath_canEnter_dict = ClientModule.get_imagePath_canEnter_dict(imagePath_plateSqlID_dict,
                                                                               licencePlateContent_plateSqlID_dict,
                                                                               plates)
            decisions_handler.insert_decisions(imagePath_plateSqlID_dict, imagePath_canEnter_dict)
        licencePlateContent_isPermitted_dict = {}
        for plate in plates:
            licencePlateContent_isPermitted_dict[plate.get_content()] = plate.is_permitted()
        return licencePlateContent_isPermitted_dict

    @staticmethod
    def get_imagePath_canEnter_dict(imagePath_plateSqlID_dict, licencePlateContent_plateSqlID_dict, plates):
        """ for internal usage/
        @:param (dict) imagePath_plateSqlID_dict -
         key: image file path.
        value: plate_id from plates table (database) that related to licence plate
        @:param (dict) licencePlateContent_plateSqlID_dict -
        key: licence plate content
        value: plate_id as saved in plates table in database
        @:param (list)  plates - list of plates objects
        @:returns (dict) imagePath_canEnter_dict
        key: image file path
        value: is the licence approved?
        """
        plateSqlID_canEnter_dict = ClientModule.get_plateSqlId_canEnter_dict(licencePlateContent_plateSqlID_dict,
                                                                             plates)
        imagePath_canEnter_dict = {}
        for imagePath in imagePath_plateSqlID_dict:
            imagePath_canEnter_dict[imagePath] = plateSqlID_canEnter_dict.get(imagePath_plateSqlID_dict.get(imagePath))
        return imagePath_canEnter_dict

    @staticmethod
    def get_plateSqlId_canEnter_dict(licencePlateContent_plateSqlID_dict, plates):
        """ for internal usage/
        @:param (dict) licencePlateContent_plateSqlID_dict -
         key: licencePlateContent.
        value: plate_id from plates table (database)
        @:param (list)  plates - list of plates objects
        @:returns (dict) plateSqlId_canEnter_dict
        key: plate_id of the plate from plates table (database)
        value: is the vehicle approved to enter
        """
        plateSqlID_canEnter_dict = {}
        for plate in plates:
            plateSqlID_canEnter_dict[
                licencePlateContent_plateSqlID_dict.get(plate.get_content())] = plate.is_permitted()
        return plateSqlID_canEnter_dict

    @staticmethod
    def get_imagePath_plateSqlID_dict(licencePlateContent_plateSqlID_dict, licencePlateContent_imagePath_dict):
        """ for internal usage/
        @:param (dict) licencePlateContent_plateSqlID_dict -
         key: licencePlateContent.
        value: plate_id from plates table (database)
        @:param (dict)  licencePlateContent_imagePath_dict -
        key: licencePlateContent
        value: image path from which we made a decision
        @:returns (dict) imagePath_plateSqlID_dict
        key: image path.
        value: plate_id
        """
        imagePath_plateSqlID_dict = {}
        for content in licencePlateContent_imagePath_dict:
            imagePath_plateSqlID_dict[licencePlateContent_imagePath_dict[content]] = \
                licencePlateContent_plateSqlID_dict[EntryDecider.remove_all_white_spaces(content)]
        return imagePath_plateSqlID_dict

@app.route('/insert_car', methods=['POST'])
def insert_car():
    """
    @:param path (str) - required - the path of the image
    @:returns if the vehicle is valid to enter the parking lot
    """
    path = request.json['path']
    license_plate_content = ImageInfoExtractor.parse_image_text(path)
    if not license_plate_content:
        return jsonify({"message:": "could not find any image in path"}), NOT_FOUND
    plate = EntryDecider.get_plate(license_plate_content)
    license_plate_content = EntryDecider.remove_all_white_spaces(license_plate_content)
    plates_handler.insert_plate(plate)
    plateID = plates_handler.select_plate(license_plate_content)
    decisions_handler.insert_decision(path, plateID, plate.is_permitted())
    if not plate.is_permitted():
        return jsonify({"message": "Car is not permitted"}), OK
    else:
        return jsonify({"message": "Car is permitted"}), OK


@app.route('/insert_batch_cars', methods=['POST'])
def insert_batch_cars():
    """
    @:param path (str) - required - the path of the images directory
    @:returns decision for each detected licence plate
    """
    directory_path = request.json['path']
    licencePlateContent_isPermitted_dict = ClientModule.add_images_from_path(directory_path)
    if licencePlateContent_isPermitted_dict is None:
        return jsonify({"message:": "could not find any images in path"}), NOT_FOUND
    message = {
        'message': 'OK',
        'decisions': licencePlateContent_isPermitted_dict
    }
    return jsonify(message)


@app.route('/get_last_week_rejected_vehicles', methods=['GET'])
def get_last_week_rejected_vehicles():
    """
    @:returns a json consists of the last week rejected vehicles
    """
    vehicles = ClientModule.get_last_week_declined_vehicles()
    if not vehicles:
        jsonify({"message:": "could not find any rejected vehicles last week"}), NOT_FOUND
    message = {'message': 'OK', 'vehicles': [vehicle.serialize() for vehicle in vehicles]}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)



