import math

from Position import positionClass


class EnemyMissileClass(object):

    def __init__(self, pos, ObjPosition, id):
        self.id = id
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.ObjectivePosition = positionClass(ObjPosition.positionX, ObjPosition.positionY, ObjPosition.positionZ)
        self.orientation = self.getObjectiveDirection(pos, ObjPosition)
        self.velocity = 2
        self.objectiveImpacted = False
        self.intercepted = False
        self.objectiveStillAlive = False
        self.difPositionWithObjectivePosition = (0, 0, 0)
        self.moduleObjectivePosition = 0
        self.normalizePositionObjectiveVector = (0, 0, 0)
        self.calculateDifferenceWithObjectivePosition()
        self.calculateModuleOfObjectivePosition()
        self.calculateNormalizeObjectivePositionVector()

    def isInObjectiveX(self):
        if self.ObjectivePosition.positionX - self.position.positionX <= 1:
            return True
        else:
            return False

    def isInObjectiveY(self):
        if self.ObjectivePosition.positionY - self.position.positionY <= 1:
            return True
        else:
            return False

    def isInObjectivePerimeter(self):
        if (abs(self.ObjectivePosition.positionX - self.position.positionX) <= 1 and
                abs(self.ObjectivePosition.positionY - self.position.positionY) <= 1):
            return True
        else:
            return False

    def isInObjectiveAltitude(self):
        if self.position.positionZ - self.ObjectivePosition.positionZ <= 1:
            return True
        else:
            return False

    def hasReachTheObjective(self):
        if self.isInObjectiveX() and self.isInObjectiveY() and self.isInObjectiveAltitude():
            self.objectiveImpacted = True

    def hasBeenIntersected(self):
        self.intercepted = True

    def getObjectiveImpacted(self):
        return self.objectiveImpacted

    def getIntercepted(self):
        return self.intercepted

    def getObjectiveDirection(self, myPosition, ObjPosition):
        direction = {"x": 1, "y": 1}

        if ObjPosition.positionX - myPosition.positionX > 0:
            direction["x"] = 1
        else:
            direction["x"] = -1

        if ObjPosition.positionY - myPosition.positionY > 0:
            direction["y"] = 1
        else:
            direction["y"] = -1

        return direction

    def goToObjective(self):
        if not self.objectiveImpacted and not self.intercepted:
            if abs(self.ObjectivePosition.positionX - self.position.positionX) > 1:
                self.position.positionX += self.velocity * self.orientation[
                    "x"] * self.normalizePositionObjectiveVector.positionX
            if abs(self.ObjectivePosition.positionY - self.position.positionY) > 1:
                self.position.positionY += self.velocity * self.orientation[
                    "y"] * self.normalizePositionObjectiveVector.positionY
            if self.isInObjectivePerimeter() and not self.isInObjectiveAltitude():
                if not self.isInObjectiveX():
                    self.position.positionX += self.velocity * self.orientation[
                        "x"] * self.normalizePositionObjectiveVector.positionX
                if not self.isInObjectiveY():
                    self.position.positionY += self.velocity * self.orientation[
                        "y"] * self.normalizePositionObjectiveVector.positionY
                self.position.positionZ -= self.velocity * self.normalizePositionObjectiveVector.positionZ
            self.hasReachTheObjective()

    def calculateDifferenceWithObjectivePosition(self):
        self.difPositionWithObjectivePosition = positionClass(
            abs(self.ObjectivePosition.positionX - self.position.positionX),
            abs(self.ObjectivePosition.positionY - self.position.positionY),
            abs(self.ObjectivePosition.positionZ - self.position.positionZ))

    def calculateModuleOfObjectivePosition(self):
        self.moduleObjectivePosition = math.sqrt(
            self.difPositionWithObjectivePosition.positionX * self.difPositionWithObjectivePosition.positionX
            + self.difPositionWithObjectivePosition.positionY * self.difPositionWithObjectivePosition.positionY
            + self.difPositionWithObjectivePosition.positionZ * self.difPositionWithObjectivePosition.positionZ)

    def calculateNormalizeObjectivePositionVector(self):
        self.normalizePositionObjectiveVector = positionClass(
            self.difPositionWithObjectivePosition.positionX / self.moduleObjectivePosition,
            self.difPositionWithObjectivePosition.positionY / self.moduleObjectivePosition,
            self.difPositionWithObjectivePosition.positionZ / self.moduleObjectivePosition)
