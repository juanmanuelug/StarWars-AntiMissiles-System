from Position import positionClass


class strategicLocationsClass(object):

    def __init__(self, pos):
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.lifes = 5
        self.destroyed = False

    def strategicLocationImpacted(self):
        self.lifes -= 1
        self.isDestroyed()

    def isDestroyed(self):
        if self.lifes <= 0:
            self.destroyed = True

    def getCityStatus(self):
        return self.destroyed
