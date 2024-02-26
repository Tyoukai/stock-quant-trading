def is_star(open, close, high, low):
    """
    十字星判断， 实体长度小于总长度的10%
    :param open:
    :param close:
    :param high:
    :param low:
    :return: True：是十字星， False：不是十字星
    """
    entity = abs(open - close)
    total = abs(high - low)
    if total == 0:
        return False
    return entity / total <= 0.1
