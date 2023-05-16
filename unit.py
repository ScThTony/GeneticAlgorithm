class unit:
    def __init__(self):
        self.num = 0
        self.capacity = 0
        self.required_int = 0

    def __str__(self):
        return "{} {} {}".format(self.num, self.capacity, self.required_int)

    def __repr__(self):
        return "{} {} {}".format(self.num, self.capacity, self.required_int)