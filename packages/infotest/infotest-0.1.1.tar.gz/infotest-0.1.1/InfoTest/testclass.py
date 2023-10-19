def test_function(x, y=None):
    """
    Test function
    :param x: x int
    :param y: y int or None
    :return: sum x + y
    """
    result_sum = x
    if y:
        result_sum += y
    return result_sum
