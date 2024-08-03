from osmnx.geocoder import geocode

class SalesRep():
    def __init__(self, name: str, home_address, vpi: float):
        self.name = name
        self.home_location = geocode(home_address)
        self.vpi = vpi
        self.allocated_leads = []
        self.available = True
        self.empty_timeslots = [7, 10, 13, 16, 19]