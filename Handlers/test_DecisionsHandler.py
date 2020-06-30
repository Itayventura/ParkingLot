import unittest
from DecisionsHandler import DecisionsHandler
import mysql.connector
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
        self.decisionsHandler = DecisionsHandler(repository)

    def test_insert_decisions(self):
        path_plateID_dict = {"test path": 158}
        path_canEnter_dict = {"test path": 0}
        self.decisionsHandler.insert_decisions(path_plateID_dict, path_canEnter_dict)

    def test_delete_decisions(self):
        self.decisionsHandler.delete_decision("test path")

    def test_insert_decision(self):
        self.decisionsHandler.insert_decision("test path", 158, 0)



if __name__ == '__main__':
    unittest.main()
