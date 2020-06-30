

sql_select = "SELECT plates.content, plates.`type`, decisions.file_source, decisions.is_url, decisions.created_at " \
             "FROM  plates, decisions " \
             "WHERE decisions.`can_enter` = 0 AND " \
             "      DATE(created_at) > DATE_SUB(now(), INTERVAL 8 DAY) AND " \
             "      plates.id = decisions.plate_id " \
             "ORDER BY plates.id, decisions.created_at"


class VehiclesHandler:

    def __init__(self, repository):
        self.repository = repository

    def select_vehicles(self):
        return self.repository.select_vehicles(sql_select)



