import math

class Vector():
    """Represents a vector in 2-dimensional space"""
	
    def __init__(self, magnitude, bearing):
        self.magnitude = magnitude
        self.bearing = bound(bearing, 0, 360)
		
    def components(self):
        return([(self.magnitude * math.cos(math.radians(self.bearing))), (self.magnitude * math.sin(math.radians(self.bearing)))])

    def resultant_vector(self, vect2):
        new_vect = Vector(0, 0)
        if self.magnitude == 0:
            new_vect = vect2
        else:
            new_vect.magnitude = math.sqrt(math.pow(self.magnitude, 2) + math.pow(vect2.magnitude, 2) - (2 * self.magnitude * vect2.magnitude * math.cos(math.radians(180 - (vect2.bearing - self.bearing)))))
            new_components = [(self.magnitude * math.cos(math.radians(self.bearing)) + (vect2.magnitude * math.cos(math.radians(vect2.bearing)))), (self.magnitude * math.sin(math.radians(self.bearing)) + (vect2.magnitude * math.sin(math.radians(vect2.bearing))))]
            if new_vect.magnitude == 0:
                new_vect.bearing = self.bearing
            else:
                if new_components[0] == 0:
                    if new_components[1] < 0:
                        new_vect.bearing = 180
                    else:
                        new_vect.bearing = -180
                elif new_components[0] < 0:
                    new_vect.bearing = math.degrees(math.atan(new_components[1] / new_components[0])) + 180
                else:
                    new_vect.bearing = math.degrees(math.atan(new_components[1] / new_components[0]))
        return(new_vect)

def clean_cos(cos_angle):
    return min(1,max(cos_angle,-1))

def bound(value, low, high):
    diff = high - low
    return (((value - low) % diff) + low)
