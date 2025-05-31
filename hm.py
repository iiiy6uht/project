class Animal:
    def __init__(self):
        self.wool = 1

    def view(self):
        return 'various'


class Rabbit(Animal):
    def __init__(self):
        super().__init__()
        self.herbivorous = 1

    def jump_m(self):
        return '1.5'


rabbit = Rabbit()
