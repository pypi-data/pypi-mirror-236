from typing import Any


class StepContextManager:
    def __init__(self, title: str):
        self.title = title

    def __enter__(self):
        print(self.title)

    def __exit__(self, exc_type, exc_value, traceback):
        print("成功!")
        if exc_type is not None:
            print(f"An exception occurred: {exc_type}, {exc_value}")


class StepManager:
    index = 1

    def step(self, title: str):
        context_manager = StepContextManager(f"Step {self.index}: {title}")
        self.index += 1
        return context_manager

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.step(*args)
