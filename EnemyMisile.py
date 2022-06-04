from Position import positionClass


class EnemyMisileClass(object):

    def __init__(self, pos, ObjPosition):
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.ObjectivePosition = positionClass(ObjPosition.positionX, ObjPosition.positionY, ObjPosition.positionZ)
        self.orientation = self.getObjectiveDirection(pos, ObjPosition)
        self.velocity = 0.001
        self.exploted = False
        self.difPositionWithObjectivePosition = positionClass(
            abs(self.ObjectivePosition.positionX - self.position.positionX),
            abs(self.ObjectivePosition.positionY - self.position.positionY),
            abs(self.ObjectivePosition.positionZ - self.position.positionZ))

    def isInObjectiveX(self):
        if(self.ObjectivePosition.positionX - self.position.positionX < 5):
            return True
        else:
            return False

    def isInObjectiveY(self):
        if(self.ObjectivePosition.positionY - self.position.positionY < 5):
            return True
        else:
            return False

    def isInObjectivePerimeter(self):
        if (abs(self.ObjectivePosition.positionX - self.position.positionX) <= 10 and
            abs(self.ObjectivePosition.positionY - self.position.positionY) <= 10):
            return True
        else:
            return False

    def isInObjectiveAltitude(self):
        if(abs(self.ObjectivePosition.positionZ - self.position.positionZ) <= 5):
            return True
        else:
            return False

    def hasReachTheObjective(self):
        if(self.isInObjectiveX() and self.isInObjectiveY() and self.isInObjectiveAltitude()):
            self.exploted = True

    def hasBeenIntersected(self):
        self.exploted = True

    def getObjectiveDirection(self,myPosition, ObjPosition):
        direction = {"x": 1, "y": 1}

        if (ObjPosition.positionX - myPosition.positionX > 0):
            direction["x"] = 1
        else:
            direction["x"] = -1

        if (ObjPosition.positionY - myPosition.positionY > 0):
            direction["y"] = 1
        else:
            direction["y"] = -1

        return direction

    def goToObjective(self):
        if not self.exploted:
            if(abs(self.ObjectivePosition.positionX - self.position.positionX) > 10):
                self.position.positionX += self.velocity * self.orientation["x"] * self.difPositionWithObjectivePosition.positionX
            if(abs(self.ObjectivePosition.positionY - self.position.positionY) > 10):
                self.position.positionY += self.velocity * self.orientation["y"] * self.difPositionWithObjectivePosition.positionY
            if(self.isInObjectivePerimeter() and not self.isInObjectiveAltitude()):
                if not self.isInObjectiveX():
                    self.position.positionX += self.velocity * self.orientation["x"] * self.difPositionWithObjectivePosition.positionX
                if not self.isInObjectiveY():
                    self.position.positionY += self.velocity * self.orientation["y"] * self.difPositionWithObjectivePosition.positionY
                self.position.positionZ -= self.velocity * self.difPositionWithObjectivePosition.positionZ
            self.hasReachTheObjective()


