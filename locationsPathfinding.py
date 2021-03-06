#todo make ##todo make #todo make this more general
import maya.cmds as cmds
import random
import collections
import heapq
#delete existing cubes
cubeLs = cmds.ls('myCube*', tr=True)
if len(cubeLs) > 0:
    cmds.delete(cubeLs)

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        SquareGrid.__init__(self, width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)



class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start) # optional
    path.reverse() # optional
    return path

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far
#make cube
def createCube():
    cube = cmds.polyCube(name='myCube#')[0]
    cmds.move(0,0.5,0, cube, r=True)
    #make pivot attr keyable
    cmds.setAttr("%s.rotatePivotTranslateY" % cube, k=True)
    cmds.setAttr("%s.rotatePivotTranslateX" % cube, k=True)
    cmds.setAttr("%s.rotatePivotTranslateZ" % cube, k=True)
    cmds.setAttr("%s.scalePivotX" % cube, k=True)
    cmds.setAttr("%s.scalePivotY" % cube, k=True)
    cmds.setAttr("%s.scalePivotZ" % cube, k=True)
    cmds.setAttr("%s.rotatePivotX" % cube, k=True)
    cmds.setAttr("%s.rotatePivotY" % cube, k=True)
    cmds.setAttr("%s.rotatePivotZ" % cube, k=True)
    cmds.setAttr("%s.scalePivotTranslateX" % cube, k=True)
    cmds.setAttr("%s.scalePivotTranslateY" % cube, k=True)
    cmds.setAttr("%s.scalePivotTranslateZ" % cube, k=True)

def roundCoords(coords):
    for i in range(len(coords)):
        coords[i] = round(coords[i]*2)/2
    return coords

def getCubePos(cubeTrans):
    coords = cmds.xform(cubeTrans, q=True, t=True, os=True)
    return roundCoords(coords)

def getLastKeyframe(cubeTrans): #return 0 if no keyframe (translateX) associated to object
    try:
        return cmds.keyframe('%s.translateX' % cubeTrans, q=True)[-1]
    except:
        return 0


def rollCube(vect, startTime, stepTime, cubeTrans):
    endTime = startTime + stepTime
    z,y,x = vect
    xRot,yRot,zRot = x*90, y*90, z*(-90)
    xHalf, yHalf, zHalf = x*0.5, y*0.5, z*0.5
    #print(x,y,z,xHalf,yHalf,zHalf,xRot,yRot,zRot)
    #centres pivot, and cube orientation reset, then moves y pivot down
    cmds.xform(cubeTrans, centerPivots=True)
    cmds.rotate(0,0,0,cubeTrans)
    if y == 0:
        cmds.move(0,-0.5,0,'%s.scalePivot' % cubeTrans, '%s.rotatePivot' % cubeTrans, r=True)
    else:
        cmds.move(0,0.5,0,'%s.scalePivot' % cubeTrans, '%s.rotatePivot' % cubeTrans, r=True)
        xRot = xRot*2
        zRot = zRot*2
    #put pivot on the correct bottom edge
    cmds.move(zHalf,0,xHalf,'%s.scalePivot' % cubeTrans, '%s.rotatePivot' % cubeTrans, r=True)
    #work out the startPos

    coords = getCubePos(cubeTrans)

    cmds.setKeyframe(cubeTrans, time=startTime)
    cmds.rotate(xRot,0,zRot, cubeTrans, r=True)
    cmds.setKeyframe(cubeTrans, time=endTime-1)
    cmds.xform(cubeTrans, centerPivots=True)
    cmds.rotate(0,0,0,cubeTrans)
    cmds.setKeyframe(cubeTrans, time=endTime)
    return getCubePos(cubeTrans)

    # #cube has moved, z-=1, so move the pivot accordingly
    # cmds.move(0,0,-1,'myCube1.scalePivot', 'myCube1.rotatePivot', r=True)
    # cmds.setKeyframe(cube, time=21)
    # cmds.rotate(-90,0,0, cube, r=True)
    # cmds.setKeyframe(cube, time=42)
    # cmds.xform(cubeTrans, centerPivots=True)



def moveCube(targetPos, cube, step):
    currentPos = getCubePos(cube)
    if currentPos[0] < targetPos[0]:
        currentPos = rollCube([1,0,0],getLastKeyframe(cube)+1,step,cube)
    elif currentPos[0] > targetPos[0]:
        currentPos = rollCube([-1,0,0],getLastKeyframe(cube)+1,step,cube)
    elif currentPos[2] < targetPos[2]:
        currentPos = rollCube([0,0,1],getLastKeyframe(cube)+1,step,cube)
    elif currentPos[2] > targetPos[2]:
        currentPos = rollCube([0,0,-1],getLastKeyframe(cube)+1,step,cube)
    print(currentPos)
        #break if cube is in target position
    if currentPos[0] == targetPos[0] and currentPos[1] == targetPos[1] and currentPos[2] == targetPos[2]:
        return 1
    else:
        return 0

def uniqueXZ(checkList):
    while True:
        x = random.randrange(0,20)
        z = random.randrange(0,20)
        if (x,z) not in checkList:
            break
    return x,z


diagram4 = GridWithWeights(20, 20)
'''
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8), (1,1), (1,2), (1,3),(0,0)]
diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}
'''
cubesInFinalPos = {} #dict for each cube, True if in final position
cubesStartPos = {}
cubesGoalPos = {}
#make 30 cubes
for i in range(0,30):
    createCube()
#move all cubes to a unique x/z position and add all cubes as walls
for cube in cmds.ls('myCube*', tr=True):
    cubesInFinalPos[cube] = False
    x,z = uniqueXZ(diagram4.walls)
    cmds.move(x,0,z, cube, r=True)
    cubesStartPos[cube] = tuple(getCubePos(cube)[::2])
    diagram4.walls.append(tuple(getCubePos(cube)[::2]))
    while True:
        cubesGoalPos[cube] = tuple(uniqueXZ(cubesGoalPos))
        if cubesGoalPos[cube] != cubesStartPos[cube]:
            break

cube = 'myCube1'


came_from, cost_so_far = a_star_search(diagram4, cubesStartPos[cube], cubesGoalPos[cube])
path = reconstruct_path(came_from, cubesStartPos[cube], cubesGoalPos[cube])

while path != []:
    cubePos = tuple(getCubePos('myCube1')[::2])
    nextMove = path.pop(0)
    print("currentPos:",cubePos, " nextMove", nextMove, cubePos==nextMove)
    if nextMove == cubePos:
        print('Next move is cubepos already')
    else:
        xMove = nextMove[0] - cubePos[0]
        zMove = nextMove[1] - cubePos[1]
        rollCube([xMove,0,zMove],getLastKeyframe('myCube1')+1,10,'myCube1')
print("Cube reached destination")
