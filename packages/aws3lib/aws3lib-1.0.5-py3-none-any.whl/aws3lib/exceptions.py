class ObjectMustBeNotNull(Exception):
    def __init__(self):
        super().__init__("Object must be not null")

class PolicyMustBeNotNull(Exception):
    def __init__(self):
        super().__init__("Policy must be not null")