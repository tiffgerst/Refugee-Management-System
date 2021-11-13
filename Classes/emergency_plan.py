

class EmergencyPlan:
    def __init__(self, em_plan_id = int, camps_count = int, type = str, description = str, geo_area = str, start_date = str, end_date = None):
    #end_date -> optional => default set to None

        self.em_plan_id = em_plan_id
        self.camps_count = camps_count
        self.type = type
        self.description = description
        self.geo_area = geo_area
        self.start_date = start_date
        self.end_date = end_date

    def create(self):
        """
        Save new row to CSV file
        """
        pass

    def display_summary(self):
        pass
