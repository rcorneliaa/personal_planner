class ActivityServices:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_activity(self, vacation_id, day, start_time, end_time, activity, location, notest):
        if not activity.strip():
            return False, "Activity cannot be empty"
        if start_time >= end_time:
            return False, "Start time must be before end time"
        self.db.add_activity(vacation_id, day, start_time, end_time, activity, location, notest)
        return True, None
    
    def get_activities(self, vacation_id, day):
        return self.db.get_activities(vacation_id, day)
    
    def delete_activity(self, activity_id):
        if not activity_id:
            return False, "Invalid activity"
        self.db.delete_activity(activity_id)
        return True, None
    
    def update_activity(self, activity_id, start_time, end_time, activity, location, notest):
        if not activity.strip():
            return False, "Activity name required"

        if start_time >= end_time:
            return False, "Invalid time interval"

        self.db.update_activity(activity_id, start_time, end_time, activity, location, notest)

        return True, None

    