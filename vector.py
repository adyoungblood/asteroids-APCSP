import math

class Vector():
    """Represents a vector in 2-dimensional space"""
	
    def __init__(self, magnitude, bearing):
        self.magnitude = magnitude
        self.bearing = bearing % 360
		
    def components(self):
        return([(self.magnitude * math.cos(math.radians(self.bearing))), (self.magnitude * math.sin(math.radians(self.bearing)))])

    def resultant_vector(self, vect2):
        new_vect = Vector(0, 0)
        if self.magnitude == 0:
            new_vect = vect2
        else:
            new_vect.magnitude = math.sqrt(math.pow(self.magnitude, 2) + math.pow(vect2.magnitude, 2) - (2 * self.magnitude * vect2.magnitude* math.cos(math.radians(180 - (vect2.bearing - self.bearing)))))
            new_vect.bearing = self.bearing + math.degrees(math.acos(clean_cos((math.pow(new_vect.magnitude, 2) + math.pow(self.magnitude, 2) - math.pow(vect2.magnitude, 2)) / (2 * new_vect.magnitude * self.magnitude))))
        return(new_vect)

def clean_cos(cos_angle):
    return min(1,max(cos_angle,-1))
		
