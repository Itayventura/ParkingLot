import unittest
from ClientModule import ClientModule


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.clientModule = ClientModule()

    def test_print_report_last_week_declined_plates(self):
        self.clientModule.print_report_last_week_declined_plates()


if __name__ == '__main__':
    unittest.main()
