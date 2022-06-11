from Position import positionClass


class CounterMeasureSystemClass(object):
    def __init__(self, pos, id):
        self.id = id
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
