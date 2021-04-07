import gpxpy
import gpxpy.gpx

# Parsing an existing file:
# -------------------------
class gpx_parser:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.gpx_file = open(file_path, 'r')
        self.gpx = gpxpy.parse(self.gpx_file)
    
    def get_gpx_cords(self):
        gps_list = []
        for route in self.gpx.routes:
            for point in route.points:
                gps_cordinates = (point.latitude, point.longitude)
                gps_list.append(gps_cordinates)
                
        return gps_list
