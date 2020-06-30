import unittest
from API import ocr_API

URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/1956_Florida_%28USA%29_License_Plate.JPG/1200px-1956_Florida_%28USA%29_License_Plate.JPG'
broken_URL = 'dofgn'


class test_ocr_API(unittest.TestCase):

    def setUp(self):
        self.api = ocr_API()

    def test_ocr_url(self):
        parsed_text = self.api.ocr_url(URL)
        self.assertEqual(True, '68' in parsed_text)
        self.assertEqual(True, '1647' in parsed_text)

    def test_ocr_url_broken(self):
        parsed_text = self.api.ocr_url(broken_URL)
        self.assertEqual('', parsed_text)

    def test_ocr_file(self):
        parsed_text = self.api.ocr_file('../ImageInfoExtractor/images/US_Diplomatic_license_plate1.jpg')
        self.assertEqual(True, 'DTH0507' in parsed_text)

    def test_ocr_file_broken_path(self):
        parsed_text = self.api.ocr_file("bla")
        self.assertEqual('', parsed_text)

    def test_ocr_file_not_image_file(self):
        parsed_text = self.api.ocr_file('images/delete.txt')
        self.assertEqual('', parsed_text)

    def test_ocr_file_with_non_plate_image(self):
        parsed_text = self.api.ocr_file('images/non_plate.jpg')
        self.assertEqual('', parsed_text)

    def test_another_test(self):
        parsed_text = self.api.ocr_url('https://isteam.wsimg.com/ip/3983ef70-c83a-11e4-a787-f04da207780b/ols/4688_original/:/rs=w:600,h:600')
        print("parsed", parsed_text)


if __name__ == '__main__':
    unittest.main()
