from codelimit.common.SourceMeasurement import SourceMeasurement


def risk_categories(measurements: list[SourceMeasurement]):
    result = [0, 0, 0, 0]
    for m in measurements:
        if m.length <= 15:
            result[0] += m.length
        elif m.length <= 30:
            result[1] += m.length
        elif m.length <= 60:
            result[2] += m.length
        else:
            result[3] += m.length
    return result
