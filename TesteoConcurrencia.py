from EnemyMisile import EnemyMisileClass
from Position import positionClass
import multiprocessing
import random

def goToObjectivesMultiple(enemies):
    contador = 0
    for enemy in enemies:
        print(contador)
        enemy.goToObjective()
        contador+=1

if __name__ == "__main__":
    position = positionClass(200, 2, 150)
    position2 = positionClass(200, 200, 200)
    ObjPosition = positionClass(100, 150, 10)
    ObjPosition2 = positionClass(105, 155, 15)
    enemy = [EnemyMisileClass(position, ObjPosition), EnemyMisileClass(position2, ObjPosition2)]


    processes = [multiprocessing.Process(target=goToObjectivesMultiple(enemy)) for _ in range(enemy.__len__())]
    [process.start() for process in processes]
    [process.join() for process in processes]
