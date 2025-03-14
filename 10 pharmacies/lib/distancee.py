import math


def distancee(a, b):
    degree_to_meters_factor = 111 * 1000
    dolgota_a, shirota_a = a
    dolgota_b, shirota_a = b

    shirota_in_radians = math.radians((shirota_a + shirota_a) / 2.)
    dolg_shir_factor = math.cos(shirota_in_radians)

    dx = abs(dolgota_a - dolgota_b) * degree_to_meters_factor * dolg_shir_factor
    dy = abs(shirota_a - shirota_a) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance
