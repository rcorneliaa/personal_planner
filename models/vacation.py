
class Vacation:
    """
    Represents a vacation entity.

    Attributes:
        id (int): Unique identifier of the vacation
        destination (str): Vacation destination (country, city)
        start_date (str | date): Start date of the vacation
        end_date (str | date): End date of the vacation
    """

    def __init__(self, id,destination, start_date, end_date, user_id):
        self.id = id
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id 


class Itinerary:
    """
    Represents an activity planned during a vacation day.
    """
    def __init__(self, id, vacation_id, day, start_time, end_time, activity, location, notest):
        self.id = id
        self.vacation_id = vacation_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.activity = activity
        self.location = location
        self.notest = notest

