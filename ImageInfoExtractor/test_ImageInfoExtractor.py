import unittest
from ImageInfoExtractor import ImageInfoExtractor


class MyTestCase(unittest.TestCase):

    @staticmethod
    def test_parse_images_text_from_dir_path():
        d = ImageInfoExtractor.parse_images_text_from_dir_path()
        for item in d.items():
            print(item)


if __name__ == '__main__':
    unittest.main()
