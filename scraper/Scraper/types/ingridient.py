from scraper.Utils.util_types import Measurement


class parsedIngridient:
    name: str
    quantity: float
    measurement: Measurement
    text: str

    def __init__(self, name: str, quantity: float, measurement: Measurement,
                 text: str):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.text = text
