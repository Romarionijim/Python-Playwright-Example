class Steps:
    def __init__(self, step_description: str):
        self.step_description = step_description

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Step(Steps):
    pass


class Given(Steps):
    pass


class When(Steps):
    pass


class Then(Steps):
    pass
