class InvalidCarId(Exception):
    def __init__(self, message="Incorrect ID"):
        self.message = message
        super().__init__(self.message)


class RedisError(Exception):
    def __init__(self, message="Redis Error"):
        self.message = message
        super().__init__(self.message)


class CarInfoError(Exception):
    def __init__(self, message="Error trying to get car info from site"):
        self.message = message
        super().__init__(self.message)


class CalculationError(Exception):
    def __init__(self, message="Error trying to calculate car info"):
        self.message = message
        super().__init__(self.message)
