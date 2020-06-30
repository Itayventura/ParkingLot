from API.ocr_API import ocr_API
import os
import logging

logging.basicConfig(level=logging.INFO)

api = ocr_API()


class ImageInfoExtractor:

    @staticmethod
    def parse_images_text_from_dir_path(directory_path="images"):
        """
        @:param (str) directory path from which it iterates through all images, sends a request to ocrspace API
        and get plate content for each image
        @:returns (dict) key(str): licence plate content. value(str): image path
        """
        content_path_dict = {}
        try:
            for file_name in os.listdir(directory_path):
                file_path = directory_path + '/' + file_name
                image_content = ImageInfoExtractor.parse_image_text(file_path)
                if image_content is not None:
                    content_path_dict[image_content] = file_path
            return content_path_dict
        except OSError as e:
            logging.warning("could not open path")
            return None

    @staticmethod
    def parse_image_text(file_path):
        """
        @:param (str) image path, the method sends a request to ocrspace API with the image path
        and get plate content for each image
        @:returns image plate licence content
        """
        image_content = api.ocr_file(file_path)
        if image_content != "":
            image_content.replace('\r\n', '\n')
            logging.info(
                "the following content was detected by the api: " + image_content + " from this image path: " + file_path)
            return image_content
        else:
            logging.warning("the api did not succeed to detect image content from the following image path: " +
                            file_path + "\nTherefore, the decision is not saved to database")
