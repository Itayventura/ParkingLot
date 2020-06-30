import logging

import mysql.connector
from Entities.Image import PathImage, UrlImage
from Entities.Plate import Plate
from Entities.Vehicle import Vehicle

logging.basicConfig(level=logging.INFO)


class Repository:
    """
        A class used to connect and interact with a MySQL database.
        Attributes:
            cnx: The MySQL connection object.
            cursor: The MySQL cursor object which interacts with the MySQL server.
        """

    def __init__(self, cnx, cursor):
        self.cnx = cnx
        self.cursor = cursor

    def execute(self, sql_query):
        """
        @:param (str) sql_query.
        the method executes the query. the query can be of any type: insert, update, delete...
        """
        try:
            self.cursor.execute(sql_query)
            self.cnx.commit()
            logging.info(str(self.cursor.rowcount) + " rows executed successfully")
        except mysql.connector.Error as error:
            logging.error("Failed to execute query:\n" + sql_query + "\n{}".format(error))

    def select_plates(self, sql_query):
        """
        @:param (str) sql_query.
        the method executes the query. the query is of a selection query.
        the query selects plates (license content, plate type)
        @:return (dict) key: licence_plate_content. value: plate_type
        """
        content_plateId_dict = {}
        try:
            self.cursor.execute(sql_query)
            records = self.cursor.fetchall()
            logging.info(str(len(records)) + " rows selected successfully")
            for record in records:
                content_plateId_dict[record[1]] = record[0]
            return content_plateId_dict
        except Exception as e:
            logging.error("Error reading data from MySQL table" + str(e))

        finally:
            if self.cnx.is_connected():
                logging.info("MySQL connection is closed")

    def select_vehicles(self, sql_query):
        """
        @:param (str) sql_query.
        the method executes the query. the query is of a selection query.
        the query selects plates (license content, plate type) and its related images, decisions
        @:return (list) vehicles. where each vehicle contains a plate object and list of images.
        """
        vehicles = []
        try:
            self.cursor.execute(sql_query)
            records = self.cursor.fetchall()
            if len(records) < 1:
                logging.info("0 rows selected successfully")
                return vehicles
            record = records[0]
            plate = Plate(record[0], Plate.get_type_from_str(record[1]))
            images = []

            if record[3]:
                images.append(UrlImage(record[2], record[4]))
            else:
                images.append(PathImage(record[2], record[4]))

            logging.info(str(len(records)) + " rows selected successfully")
            for i in range(1, len(records)):
                record = records[i]
                if record[0] != plate.get_content():
                    vehicles.append(Vehicle(plate, images))
                    plate = Plate(record[0], Plate.get_type_from_str(record[1]))
                    images = []

                if record[3]:
                    images.append(UrlImage(record[2], record[4]))
                else:
                    images.append(PathImage(record[2], record[4]))
            vehicles.append(Vehicle(plate, images))
            return vehicles

        except Exception as e:
            logging.exception("Error reading data from MySQL table" + e)
