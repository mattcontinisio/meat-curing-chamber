import random


def read(sensor_type, pin):
    return (random.uniform(60, 90), random.uniform(0, 30))


def read_retry(sensor_type, pin):
    return (random.uniform(60, 90), random.uniform(0, 30))
