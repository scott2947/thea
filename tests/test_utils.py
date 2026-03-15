import numpy as np
from thea.utils import calculate_average


def test_calculate_average_returns_correct_values():
    frame = np.array([[[10, 20, 30], [10, 20, 30]],
                      [[10, 20, 30], [10, 20, 30]]], dtype=np.float64)

    assert calculate_average(frame) == (10, 20, 30)
