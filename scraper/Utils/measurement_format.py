from ..Utils.measurementSet import measurement_dictionary


def formatMeasurement(num: float, measurement: str):
    dic = measurement_dictionary.get(measurement)
    ratio = dic['ratio']
    new_measurement = dic['measurement']

    return num * ratio, new_measurement if len(
        new_measurement) > 0 else measurement
