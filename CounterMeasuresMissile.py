import math

from Position import positionClass


class CounterMeasuresMissileClass(object):
    def __init__(self, pos, id, counterMeasureSystemId, objPos, enemyId):
        self.position = positionClass(pos.positionX, pos.positionY, pos.positionZ)
        self.objectivePosition = positionClass(objPos[0], objPos[1], objPos[2])
        self.id = id
        self.counterMeasureSystemId = counterMeasureSystemId
        self.enemyId = enemyId
        self.velocity = 6
        self.orientation = self.getObjectiveDirection(self.position, self.objectivePosition)
        self.enemyMissileIntersected = False
        self.difPositionWithObjectivePosition = (0, 0, 0)
        self.moduleObjectivePosition = 0
        self.normalizePositionObjectiveVector = (0, 0, 0)
        self.calculateDifferenceWithObjectivePosition()
        self.calculateModuleOfObjectivePosition()
        self.calculateNormalizeObjectivePositionVector()

    def updateObjectivePosition(self, enemyMissilesAssigned):
        for enemyMissile in enemyMissilesAssigned:
            if self.enemyId == enemyMissile:
                newObjectivePosition = positionClass(enemyMissilesAssigned[enemyMissile][0],
                                                     enemyMissilesAssigned[enemyMissile][1],
                                                     enemyMissilesAssigned[enemyMissile][2])
                self.objectivePosition = newObjectivePosition
                self.orientation = self.getObjectiveDirection(self.position, self.objectivePosition)

    def isEnemyMissileIntersected(self):
        if abs(self.position.positionX - self.objectivePosition.positionX) <= 5 \
                and abs(self.position.positionY - self.objectivePosition.positionY) <= 5 \
                and abs(self.position.positionZ - self.objectivePosition.positionZ) <= 5:
            self.enemyMissileIntersected = True

    def getObjectiveDirection(self, myPosition, ObjPosition):
        direction = {"x": 1, "y": 1, "z": 1}

        if ObjPosition.positionX - myPosition.positionX > 0:
            direction["x"] = 1
        else:
            direction["x"] = -1

        if ObjPosition.positionY - myPosition.positionY > 0:
            direction["y"] = 1
        else:
            direction["y"] = -1

        if ObjPosition.positionZ - myPosition.positionZ > 0:
            direction["z"] = 1
        else:
            direction["z"] = -1
        return direction

    def goToObjective(self):
        if not self.enemyMissileIntersected:
            if abs(self.objectivePosition.positionX - self.position.positionX) > 3:
                self.position.positionX += self.velocity * self.orientation["x"] \
                                           * self.normalizePositionObjectiveVector.positionX
            if abs(self.objectivePosition.positionY - self.position.positionY) > 3:
                self.position.positionY += self.velocity * self.orientation["y"] \
                                           * self.normalizePositionObjectiveVector.positionY
            if abs(self.objectivePosition.positionZ - self.position.positionZ) > 3:
                self.position.positionZ += self.velocity * self.orientation["z"] \
                                           * self.normalizePositionObjectiveVector.positionZ
            self.isEnemyMissileIntersected()

    def calculateDifferenceWithObjectivePosition(self):
        self.difPositionWithObjectivePosition = positionClass(
            abs(self.objectivePosition.positionX - self.position.positionX),
            abs(self.objectivePosition.positionY - self.position.positionY),
            abs(self.objectivePosition.positionZ - self.position.positionZ))

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
