from kivymd.toast import toast
class VacationServices:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_vacation(self, destination, start_date, end_date):
        
        if not destination.strip():
            return False, "Destination cannot be empty"

        if start_date > end_date:
            return False, "End date must be after start date"

        self.db.add_vacation(destination, start_date, end_date)
        return True, None
    
    def get_vacations(self):
        return self.db.get_vacations()