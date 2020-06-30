from EntryDecider.EntryDecider import EntryDecider

sql_insert = "INSERT IGNORE INTO plates(plates.content, plates.`type`) VALUES"
sql_select = "SELECT id, content FROM plates WHERE content IN"
sql_delete = "DELETE from plates WHERE content IN"


class PlatesHandler:

    def __init__(self, repository):
        self.repository = repository

    def select_plate(self, content):
        if content is None:
            return None
        sql_select_plate = sql_select + "('" + content + "')"
        content_plateId_dict = self.repository.select_plates(sql_select_plate)
        if content_plateId_dict:
            return content_plateId_dict[content]

    # returns dictionary of plate contents and plate id
    def select_plates(self, contents):
        if contents is None or len(contents) < 1:
            return None
        for i, content in enumerate(contents):
            contents[i] = EntryDecider.remove_all_white_spaces(content)
        sql_select_plates = self.build_sql_query(sql_select, contents)
        return self.repository.select_plates(sql_select_plates)

    def insert_plate(self, plate):
        if plate is None:
            return None
        sql_insert_plate = sql_insert + "('" + plate.get_content() + "','" + plate.get_str_plate_type() + "')"
        self.repository.execute(sql_insert_plate)

    def insert_plates(self, plates):
        if plates is None or len(plates) < 1:
            return None
        sql_insert_plates = sql_insert
        for i in range(len(plates) - 1):
            plate = plates[i]
            sql_insert_plates += "('" + plate.get_content() + "','" + plate.get_str_plate_type() + "')" + ","
        plate = plates[len(plates) - 1]
        sql_insert_plates += "('" + plate.get_content() + "','" + plate.get_str_plate_type() + "')"
        self.repository.execute(sql_insert_plates)

    def delete_plates(self, contents):
        if contents is None or len(contents) < 1:
            return None
        sql_delete_plates = self.build_sql_query(sql_delete, contents)
        self.repository.execute(sql_delete_plates)

    def build_sql_query(self, sql_query, contents):
        sql_builder_query = sql_query + "("
        for i in range(len(contents) - 1):
            content = contents[i]
            sql_builder_query += "'" + content + "',"
        last_content = contents[len(contents) - 1]
        sql_builder_query += "'" + last_content + "'" + ")"
        return sql_builder_query





