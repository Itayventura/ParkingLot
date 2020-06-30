from enum import Enum


class PlateType(Enum):
    STARTS_WITH_U = 1
    DIPLOMAT = 2
    TRANSPORTER = 3
    TWO_LAST_DIGITS = 4
    MOTOR = 5
    REGULAR = 6


class Plate:

    def __init__(self, content, plateType):
        self.content = content
        self.plateType = plateType

    def get_content(self):
        return self.content

    def get_plate_type(self):
        return self.plateType

    @staticmethod
    def get_type_from_str(str_plate_type):
        switcher = {"STARTS_WITH_U": PlateType.STARTS_WITH_U,
                    "DIPLOMAT": PlateType.DIPLOMAT,
                    "TRANSPORTER": PlateType.TRANSPORTER,
                    "TWO_LAST_DIGITS": PlateType.TWO_LAST_DIGITS,
                    "MOTOR": PlateType.MOTOR,
                    "REGULAR": PlateType.REGULAR}
        return switcher[str_plate_type]

    def get_str_plate_type(self):
        switcher = {PlateType.STARTS_WITH_U: "STARTS_WITH_U",
                    PlateType.DIPLOMAT: "DIPLOMAT",
                    PlateType.TRANSPORTER: "TRANSPORTER",
                    PlateType.TWO_LAST_DIGITS: "TWO_LAST_DIGITS",
                    PlateType.MOTOR: "MOTOR",
                    PlateType.REGULAR: "REGULAR"}
        return switcher[self.get_plate_type()]

    def is_permitted(self):
        return self.get_plate_type() == PlateType.REGULAR

    def getReason(self):
        reason = "because its license plate"

        switcher = {
            PlateType.STARTS_WITH_U: " starts with the letter 'U', i.e the vehicle belongs to the US marine corps",
            PlateType.DIPLOMAT: " starts with the letter 'D', i.e belongs to a diplomat",
            PlateType.TRANSPORTER: " starts with the letter 'G', i.e the vehicle is a transporter",
            PlateType.TWO_LAST_DIGITS: "'s last two digits are: 85/86/87/88/89/00",
            PlateType.MOTOR: " consists of E, K, L, N and R used as first letters in the 1234AB serial format. i.e the vehicle is a motorcycle",
            PlateType.REGULAR: " does not violate the parking lot rules",
        }
        return reason + switcher.get(self.plateType)

    def entrance_describer(self):
        canEnter = dict.fromkeys([PlateType.STARTS_WITH_U,
                                  PlateType.DIPLOMAT,
                                  PlateType.TRANSPORTER,
                                  PlateType.TWO_LAST_DIGITS,
                                  PlateType.MOTOR], 'cannot ')
        canEnter[PlateType.REGULAR] = 'can '
        return canEnter.get(self.plateType) + 'enter the parking lot '

    def __str__(self):
        return 'The vehicle with plate content:\n' + self.get_content() + "\n" + \
               self.entrance_describer() +\
               self.getReason() + '\n'







