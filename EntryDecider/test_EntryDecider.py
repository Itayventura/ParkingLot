import unittest
from EntryDecider import EntryDecider
from Entities.Plate.Plate import Plate, PlateType

contents = ['JUN\n7SUE187',
            '— FLORIDA\n—TRANSPORTER—',
            'FLORIDA\n•,EAR\nMARINE CORPS',
            'DIPLOMA T Cur-M\nDTH0507\ni 5-10',
            '456789234',
            'FLORIDA\n1112EB\nFLORIDA',
            'MAINE\n8738 LX\nhåéåiionland']


class MyTestCase(unittest.TestCase):

    def test_EntryDecider(self):
        plates = EntryDecider.get_plates(contents)
        self.assertEqual(plates[0].get_plate_type(), PlateType.TWO_LAST_DIGITS)
        self.assertEqual(plates[1].get_plate_type(), PlateType.TRANSPORTER)
        self.assertEqual(plates[2].get_plate_type(), PlateType.STARTS_WITH_U)
        self.assertEqual(plates[3].get_plate_type(), PlateType.DIPLOMAT)
        self.assertEqual(plates[4].get_plate_type(), PlateType.REGULAR)
        self.assertEqual(plates[5].get_plate_type(), PlateType.MOTOR)
        self.assertEqual(plates[5].get_plate_type(), PlateType.MOTOR)


if __name__ == '__main__':
    unittest.main()
