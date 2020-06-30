from PlatesHandler import PlatesHandler
import unittest
import mysql.connector
import logging

from Entities.Plate.Plate import Plate, PlateType
from Repository.Repository import Repository


class MyTestCase(unittest.TestCase):
    def setUp(self):
        cnx = mysql.connector.connect(host='localhost',
                                      database='parking_lot',
                                      user='root',
                                      password='1234',
                                      port='3306')
        cursor = cnx.cursor()
        repository = Repository(cnx, cursor)

        self.platesHandler = PlatesHandler(repository)

    def test_insert_plates(self):
        plates = [Plate("test content1", PlateType.STARTS_WITH_U),
                  Plate("test content2", PlateType.DIPLOMAT),
                  Plate("test content2", PlateType.DIPLOMAT),
                  Plate("test content3", PlateType.TRANSPORTER),
                  Plate("test content7", PlateType.TWO_LAST_DIGITS),
                  Plate("test content8", PlateType.MOTOR),
                  Plate("test content9", PlateType.REGULAR)
                  ]
        self.platesHandler.insert_plates(plates)

    def test_delete_plate(self):
        contents = ["test content1",
                    "test content2",
                    "test content3",
                    "test content7",
                    "test content8",
                    "test content9"]
        self.platesHandler.delete_plates(contents)

    def test_select_plates(self):
        contents = ["test content1",
                    "test content2",
                    "test content3",
                    "test content7",
                    "test content8",
                    "test content9"]
        content_plateId_dict = self.platesHandler.select_plates(contents)
        for item in content_plateId_dict.items():
            logging.info(item)


if __name__ == '__main__':
    unittest.main()
