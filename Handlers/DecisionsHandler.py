
sql_insert = "insert into decisions (file_source, plate_id, can_enter) VALUES "
sql_delete = "DELETE from decisions WHERE file_source = "


class DecisionsHandler:

    def __init__(self, repository):
        self.repository = repository

    def insert_decisions(self, path_plateID_dict, imagePath_canEnter_dict):
        sql_insert_images = sql_insert
        for path, plateID in path_plateID_dict.items():
            sql_insert_images += "('" + path + "', " + str(plateID) + ", " + str(imagePath_canEnter_dict[path]) +  ")" + ","
        self.repository.execute(sql_insert_images[:len(sql_insert_images) - 1])

    def insert_decision(self, path, plateId, can_enter):
        sql_insert_images = sql_insert + "('" + path + "', " + str(plateId) + ", " + str(can_enter) + ")"
        self.repository.execute(sql_insert_images)

    def delete_decision(self, file_source):
        self.repository.execute(sql_delete + "'" + file_source + "'")





