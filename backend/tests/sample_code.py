
import math
from pathlib import Path


def calculate_area(radius):
    return math.pi * radius ** 2


async def fetch_data():
    return {"status": "success"}


class Circle:
    def __init__(self, radius):
        self.radius = radius

    def diameter(self):
        return self.radius * 2
