from Entities.Plate import Plate, PlateType
import re
import logging

logging.basicConfig(level=logging.INFO)


class EntryDecider:

    @staticmethod
    def get_plates(contents):
        """
        @:param contents (list) - required - list of licence plate contents.
        @:returns plates (list) - list of plate objects where each plate contains plate content & plate type
        """
        plates = []
        for content in contents:
            plates.append(EntryDecider.get_plate(str(content)))
        return plates

    @staticmethod
    def get_plate(content):
        """
        @:param content (str) - required - licence plate contents
        the method decides for each licence plate its type
        @:returns plate (Plate) - plate object that contains plate content & plate type
        """
        sentences = EntryDecider.break_into_sentences(content)
        words = EntryDecider.break_into_words(content)
        if EntryDecider.starts_with_U(words, sentences):
            logging.info("\nthe plate with the following content:\n" + content + "\nis identified as STARTS_WITH_U")
            return Plate(EntryDecider.remove_all_white_spaces(content), PlateType.STARTS_WITH_U)
        elif EntryDecider.diplomat(words, sentences):
            logging.info("\nthe plate with the following content:\n" + content + "\nis identified as DIPLOMAT")
            return Plate(EntryDecider.remove_all_white_spaces(content), PlateType.DIPLOMAT)
        elif EntryDecider.transporter(words, sentences):
            logging.info("\nthe plate with the following content:\n" + content + "\nis identified as TRANSPORTER")
            return Plate(EntryDecider.remove_all_white_spaces(content), PlateType.TRANSPORTER)
        elif EntryDecider.two_last_digits(sentences):
            logging.info("\nthe plate with the following content:\n" + content + "\nis identified as TWO_LAST_DIGITS")
            return Plate(EntryDecider.remove_all_white_spaces(content), PlateType.TWO_LAST_DIGITS)
        elif EntryDecider.motor(sentences):
            logging.info("\nthe plate with the following content:\n" + content + "\nis identified as MOTOR")
            return Plate(EntryDecider.remove_all_white_spaces(content), PlateType.MOTOR)
        else:
            logging.info("\nthe plate with the following content:\n" + content + "\nis identified as REGULAR")
            return Plate(EntryDecider.remove_all_white_spaces(content), PlateType.REGULAR)

    @staticmethod
    def break_into_words(text):
        return re.findall(r"[\w']+", text)

    @staticmethod
    def break_into_sentences(text):
        return re.split('\n', text)

    @staticmethod
    def remove_all_white_spaces(text):
        return " ".join(re.findall(r"[\w']+", text)).replace("'", "")

    @staticmethod
    def starts_with_U(words, sentences):
        if 'MARINE' in words or \
                'CORPS' in words:
            return True
        if len(sentences) > 1:
            words = EntryDecider.break_into_words(sentences[len(sentences) - 2])
            if len(words) > 0 and words[0].startswith('U'):
                return True
        return False

    @staticmethod
    def diplomat(words, sentences):
        if 'DIPLOMAT' in words:
            return True
        if len(sentences) > 1:
            words = EntryDecider.break_into_words(sentences[1])
            if len(words) > 0 and words[0].startswith('D'):
                return True
        return False

    @staticmethod
    def transporter(words, sentences):
        if 'TRANSPORTER' in words:
            return True
        if len(sentences) > 1:
            words = EntryDecider.break_into_words(sentences[len(sentences) - 2])
            if len(words) > 0 and words[0].startswith('G'):
                return True
        return False

    @staticmethod
    def two_last_digits(sentences):
        if len(sentences) > 1:
            words = EntryDecider.break_into_words(sentences[1])
            if len(words) > 0 and words[len(words) - 1].endswith('85') or \
                    len(words) > 0 and words[len(words) - 1].endswith('86') or \
                    len(words) > 0 and words[len(words) - 1].endswith('87') or \
                    len(words) > 0 and words[len(words) - 1].endswith('88') or \
                    len(words) > 0 and words[len(words) - 1].endswith('89') or \
                    len(words) > 0 and words[len(words) - 1].endswith('00'):
                return True

        return False

    @staticmethod
    def motor(sentences):
        if len(sentences) > 1:
            word = sentences[1].replace(" ", "")
            possible_values = {'L', 'K', 'E', 'N'}
            if len(word) > 4 and \
                    word[0].isdigit() and \
                    word[1].isdigit() and \
                    word[2].isdigit() and \
                    word[3].isdigit() and \
                    word[4] in possible_values:
                return True
        return False
