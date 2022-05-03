import numpy as np
def discretize_angle(angle): 
        # TODO CREO que angle tmb puede ser negativo, a chequear
        if angle < 0:
            angle+=180
            print("new angle = ",angle)
        if (angle >= 0 and angle <= 22.5) or (angle >= 157.5 and angle <= 180): 
            discretized_angle = 0
        
        elif angle > 22.5 and angle <= 67.5:
            discretized_angle = 45 
        
        elif angle > 67.5 and angle <= 112.5:
            discretized_angle = 90
        
        else: 
            discretized_angle = 135 

        return discretized_angle

dx = 0
dy = -1

angle = np.arctan2(dy,dx)* 180/np.pi
x = np.cos(np.deg2rad(angle))
y = np.sin(np.deg2rad(angle))
print(f" x = {x} , y = {y}")
x = np.sign(x) * np.ceil(np.abs(x))

y = np.sign(y) * np.ceil(np.abs(y))
print(f" x = {x} , y = {y}")

print(f"angle = {angle }º")


print(f"discretized = {discretize_angle(angle)}")
