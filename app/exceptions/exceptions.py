class InvalidCarId(Exception):
    def __init__(self, message="Incorrect ID") -> None:
        self.message = message
        super().__init__(self.message)


class RedisError(Exception):
    def __init__(self, message="Redis Error") -> None:
        self.message = message
        super().__init__(self.message)


class CarInfoError(Exception):
    def __init__(self, message="Error trying to get car info from site") -> None:
        self.message = message
        super().__init__(self.message)


class CalculationError(Exception):
    def __init__(self, message="Error trying to calculate car info") -> None:
        self.message = message
        super().__init__(self.message)
