class Walker():
    def __init__(self, name, description, position, target):
        self.name = name
        self.description = description
        self.position = position
        self.target = target

    def get_name(self):
        return self.name

    def set_name(self, newName):
        self.name = newName
        
    def get_description(self):
        return self.description

    def set_description(self, newDescription):
        self.description = newDescription

    def get_position(self):
        return self.position

    def set_position(self, newPos):
        self.position = newPos

    def get_target(self):
        return self.target
    
    def set_target(self, newTarget):
        self.target = newTarget

    def walk(self):
        pass

class Immigrant(Walker):
    def __init__(self, name, description, position, target):
        super().__init__(self, name, description, position, target)

    def walk(self):
        '''tout droit vers la target'''
        pass


class Worker(Walker):
    def __init__(self, name, description, position, target, radius, typeEffect):
        super().__init__(self, name, description, position, target)
        self.radius = radius

    def get_radius(self):
        return self.radius
    
    def set_radius(self, newRadius):
        self.radius = newRadius


    def walk(self):
        pass

class Prefects(Worker):
    def __init__(self, name, description, position, target, radius):
        super().__init__(self, name, description, position, target, radius)