from VehiclesHandler import VehiclesHandler
import unittest
import mysql.connector
import logging

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

        self.vehiclesHandler = VehiclesHandler(repository)

    def test_select_vehicles(self):
        vehicles = self.vehiclesHandler.select_vehicles()
        for vehicle in vehicles:
            logging.info(vehicle)


if __name__ == '__main__':
    unittest.main()
