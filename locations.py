#todo make ##todo make #todo make this more general
import maya.cmds as cmds
#delete existing cubes
cubeLs = cmds.ls('myCube*', tr=True)
if len(cubeLs) > 0:
    cmds.delete(cubeLs)


#make cube
cube = cmds.polyCube(name='myCube#')[0]
#Put cube above grid
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

    coords = roundCoords(getCubePos(cubeTrans))
    #print("Start Pos:" + str(coords))
    #print("Moving: ", z,y,x)

    cmds.setKeyframe(cubeTrans, time=startTime)
    cmds.rotate(xRot,0,zRot, cubeTrans, r=True)
    cmds.setKeyframe(cubeTrans, time=endTime)

    #Work out the end position
    for i in range(len(coords)):
        coords[i] += vect[i]
    return coords

    # #cube has moved, z-=1, so move the pivot accordingly
    # cmds.move(0,0,-1,'myCube1.scalePivot', 'myCube1.rotatePivot', r=True)
    # cmds.setKeyframe(cube, time=21)
    # cmds.rotate(-90,0,0, cube, r=True)
    # cmds.setKeyframe(cube, time=42)
    # cmds.xform(cubeTrans, centerPivots=True)



def moveCube(targetPos, cube, step):
    currentPos = getCubePos(cube)
    for i in range(0,50):
        if currentPos[0] < targetPos[0]:
            currentPos = rollCube([1,0,0],getLastKeyframe(cube)+1,step,cube)
        elif currentPos[0] > targetPos[0]:
            currentPos = rollCube([-1,0,0],getLastKeyframe(cube)+1,step,cube)
        elif currentPos[2] < targetPos[2]:
            currentPos = rollCube([0,0,1],getLastKeyframe(cube)+1,step,cube)
        elif currentPos[2] > targetPos[2]:
            currentPos = rollCube([0,0,-1],getLastKeyframe(cube)+1,step,cube)

        #break if cube is in target position
        if currentPos[0] == targetPos[0] and currentPos[1] == targetPos[1] and currentPos[2] == targetPos[2]:
            break


moveCube([6,0.5,3], cube, 10)
