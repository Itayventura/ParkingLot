

class Vehicle:

    def __init__(self, plate, images):
        self.plate = plate
        self.images = images

    def get_dateTimes(self):
        list = []
        for image in self.images:
            list.append(image.get_dateTime())

    def serialize(self):
        decisions = []
        for i, image in enumerate(self.images):
            decisions.append({'source': image.get_source(), 'timestamp': image.get_dateTime()})
        return {'licence_plate_content': self.plate.get_content(),
                'rejection_reason': "The vehicle " + self.plate.entrance_describer() + self.plate.getReason(),
                'denied_entries': decisions}

    def __str__(self):
        describer = self.plate.__str__() + 'The vehicle was filmed trying to enter the parking lot at:\n'
        for image in self.images:
            describer += str(image.get_dateTime()) + '\n'
        return describer

