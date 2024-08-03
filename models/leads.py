from osmnx.geocoder import geocode

class Lead():
    def __init__(self, address, time: int):
        self.location = geocode(address)
        self.address = address
        self.time = time
        self.allocated = False