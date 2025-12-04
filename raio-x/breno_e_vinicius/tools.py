import numpy as np

degree_bias=0.5
d = 0.201e-9
degree_to_lambda=np.vectorize(lambda x: 2*d*np.sin(np.deg2rad(x+degree_bias)/2))


def read_file(filepath) -> tuple[np.ndarray, np.ndarray]:
    data = open(filepath).readlines()[1:]
    x = np.array([float(line.split()[0]) for line in data])
    y = np.array([float(line.split()[1]) for line in data])
    return x, y
