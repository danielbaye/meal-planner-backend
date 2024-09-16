class Nutrition:
    caloriesGram: float
    proteinGram: float
    carbsGram: float
    fatGram: float
    saturatedFatGram: float
    saltGram: float

    def __init__(self, caloriesGram: float, proteinGram: float,
                 carbsGram: float, fatGram: float, saturatedFatGram: float,
                 saltGram: float):
        self.caloriesGram = caloriesGram
        self.proteinGram = proteinGram
        self.carbsGram = carbsGram
        self.fatGram = fatGram
        self.saturatedFatGram = saturatedFatGram
        self.saltGram = saltGram
