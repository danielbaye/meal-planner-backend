measurementList = [
    'g', 'gr', 'gram', 'ml', 'milliliter', 'clove', 'cm', 'tablespoon',
    'teaspoon', 'spoon', 'cup', 't ', 't,', 'tsp', 'tb', 'tbsp', 'c', 'pt',
    'qt', 'pint', 'quart', 'gal', 'gallon', 'ounce', 'oz', 'lb', 'pound',
    'centimeter', 'centimetre', 'inch', 'in', 'dozen', 'stalk', 'leaf', 'head',
    'bulb', 'nest', 'nests'
]

measurementList.sort(reverse=True)

measurement_dictionary = {
    '': {
        'ratio': 1,
        'measurement': ''
    },
    'gram': {
        'ratio': 1,
        'measurement': 'g'
    },
    'g': {
        'ratio': 1,
        'measurement': 'g'
    },
    'gr': {
        'ratio': 1,
        'measurement': 'g'
    },
    'milliliter': {
        'ratio': 1,
        'measurement': 'ml'
    },
    'ml': {
        'ratio': 1,
        'measurement': 'ml'
    },
    'cup': {
        'ratio': 236.588,
        'measurement': 'ml'
    },
    'tablespoon': {
        'ratio': 14.787,
        'measurement': 'ml'
    },
    'tbsp': {
        'ratio': 14.787,
        'measurement': 'ml'
    },
    'teaspoon': {
        'ratio': 4.929,
        'measurement': 'ml'
    },
    'tsp': {
        'ratio': 4.929,
        'measurement': 'ml'
    },
    'pint': {
        'ratio': 473.176,
        'measurement': 'ml'
    },
    'quart': {
        'ratio': 946.353,
        'measurement': 'ml'
    },
    'gallon': {
        'ratio': 3785.41,
        'measurement': 'ml'
    },
    'ounce': {
        'ratio': 28.3495,
        'measurement': 'g'
    },
    'oz': {
        'ratio': 28.3495,
        'measurement': 'g'
    },
    'lb': {
        'ratio': 453.592,
        'measurement': 'g'
    },
    'pound': {
        'ratio': 453.592,
        'measurement': 'g'
    },
    'inch': {
        'ratio': 10,
        'measurement': 'g'
    },
    'cm': {
        'ratio': 4,
        'measurement': 'g'
    },
    'centimeter': {
        'ratio': 4,
        'measurement': 'g'
    },
    'centimetre': {
        'ratio': 4,
        'measurement': 'g'
    },
    'dozen': {
        'ratio': 12,
        'measurement': ''
    },
    'stalk': {
        'ratio': 50,
        'measurement': 'g'
    },
    'leaf': {
        'ratio': 1,
        'measurement': ''
    },
    'head': {
        'ratio': 1,
        'measurement': ''
    },
    'bulb': {
        'ratio': 1,
        'measurement': ''
    },
    'nest': {
        'ratio': 1,
        'measurement': ''
    },
    'nests': {
        'ratio': 1,
        'measurement': ''
    },
}
