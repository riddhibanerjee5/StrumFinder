class strum:
    def __init__(self, type, time):
        self.type = type
        self.time = time
        self.chord = None

    def get_type(self):
        return self.type

    def get_time(self):
        return self.time

    def get_chord(self):
        return self.chord

def generate_strums():
    strums = {}

    for i in range(50):
        strums[40+170*i] = 'down'
        strums[67+170*i] = 'down'
        strums[93+170*i] = 'up'
        strums[143+170*i] = 'up'
        strums[160+170*i] = 'down'
        strums[193+170*i] = 'up'
        

    time = [0, 1000, 1500, 2500, 3, 3500]
    return strums, time
