class Vacation:
    def __init__(self, id,destination, start_date, end_date):
        self.id = id
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date


class Itinerary:
    def __init__(self, id, vacation_id, day, start_time, end_time, activity, location, notes):
        self.id = id
        self.vacation_id = vacation_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.activity = activity
        self.location = location
        self.notes = notes
        

        