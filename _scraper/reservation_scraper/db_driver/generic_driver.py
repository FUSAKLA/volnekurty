

class GenericDbDriver:

    def get_facility_reservations(self, facility_id: str):
        pass

    def insert_reservation(self, facility_id=None, court_id=None, reservation_start=None, reservation_end=None):
        pass
    
    def delete_all_future_facility_reservations(self, facility_id: str):
        pass
    
    def delete_all_reservations(self):
        pass
    
    def insert_facility(self, name=None, address=None, opening_time=None, closing_time=None, position_x=None, position_y=None, telephone=None, price=None):
        pass
    
    def update_facility(self, facility_id, name=None, address=None, opening_time=None, closing_time=None, position_x=None, position_y=None, telephone=None, price=None):
        pass
    
    def delete_facility(self, facility_id):
        pass
    
    def select_facility_by_name(self, name: str):
        pass
    
    def select_facility_by_id(self, facility_id: str):
        pass