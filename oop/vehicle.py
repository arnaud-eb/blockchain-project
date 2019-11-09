class Vehicle:
    def __init__(self,top_speed=100,warnings=[]):
        self.top_speed=top_speed
        self.warnings=warnings

    def drive(self):
        print(f'I am driving but certainly not faster than {self.top_speed}')

    def __str__(self):
        return f'A speed of: {self.top_speed}, and warning(s): {len(self.warnings)}'

# vehicle1=Vehicle(top_speed=100,warnings=['Insufficient Oil','Speed too high'])
# print(vehicle1.top_speed)
# print(vehicle1.warnings)
# vehicle1.drive()
# print(vehicle1)
