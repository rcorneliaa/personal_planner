from core.services.location_services import LocationServices

class VacationServices:
    """
    Service layer for managing vacations.

    Handles validation and delegates database operations for vacations.
    Also integrates LocationServices for location-related functionality.
    """
    def __init__(self, db_manager):
        self.db = db_manager
        self.location_services = LocationServices()

    def add_vacation(self, destination, start_date, end_date):
        """
        Adds a new vacation with validation.

        Returns:
            tuple[bool, str | None]: (Success flag, Error message if validation fails)
        """
        
        if not destination.strip():
            return False, "Destination cannot be empty"

        if start_date > end_date:
            return False, "End date must be after start date"

        self.db.add_vacation(destination, start_date, end_date)
        return True, None
    
    def get_vacations(self):
        """
        Retrieves all vacations from the database.
        """
        return self.db.get_vacations()