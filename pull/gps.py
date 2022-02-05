from geopy import Point                                                                                                                                                                       
from geopy.distance import geodesic    
import ee     

def get_polygon(lat, lon, distKm = 10) -> ee.Geometry.Polygon:
    def get_float(location: str):
        point = location.split(", ")
        point[0] = float(point[0])
        point[1] = float(point[1])
        return point
    
    #print(lat, lon)
    degree = 45
    north = get_float(geodesic(kilometers=distKm).destination(Point(lat, lon), 0 + degree).format_decimal())[::-1]                                                                                              
    east = get_float(geodesic(kilometers=distKm).destination(Point(lat, lon), 90 + degree).format_decimal())[::-1]                                                                                           
    south = get_float(geodesic(kilometers=distKm).destination(Point(lat, lon), 180 + degree).format_decimal())[::-1]                                                                                        
    west = get_float(geodesic(kilometers=distKm).destination(Point(lat, lon), 270 + degree).format_decimal())[::-1]
    
    polygon = ee.Geometry.Polygon([[
        west,
        north,
        east,
        south,
    ]], None, False)
    return polygon

if __name__ == "__main__":
    pass