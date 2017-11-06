#todo make ##todo make #todo make this more general
import maya.cmds as cmds

def deleteExisting(name):
    cubeLs = cmds.ls('%s*' % name, tr=True)
    if len(cubeLs) > 0:
        cmds.delete(cubeLs)

def makePivotKeyable(trans):
    cmds.setAttr("%s.rotatePivotTranslateY" % trans, k=True)
    cmds.setAttr("%s.rotatePivotTranslateX" % trans, k=True)
    cmds.setAttr("%s.rotatePivotTranslateZ" % trans, k=True)
    cmds.setAttr("%s.scalePivotX" % trans, k=True)
    cmds.setAttr("%s.scalePivotY" % trans, k=True)
    cmds.setAttr("%s.scalePivotZ" % trans, k=True)
    cmds.setAttr("%s.rotatePivotX" % trans, k=True)
    cmds.setAttr("%s.rotatePivotY" % trans, k=True)
    cmds.setAttr("%s.rotatePivotZ" % trans, k=True)
    cmds.setAttr("%s.scalePivotTranslateX" % trans, k=True)
    cmds.setAttr("%s.scalePivotTranslateY" % trans, k=True)
    cmds.setAttr("%s.scalePivotTranslateZ" % trans, k=True)


def rollCube(vect, startTime, endTime, cubeTrans):
    x,y,z = vect
    xRot,yRot,zRot = x*90, y*90, z*(-90)
    xHalf, yHalf, zHalf = x*0.5, y*0.5, z*0.5 #weird things happen using /2 instead of *0.5 (mayabug works in python)
    print(x,y,z,xHalf,yHalf,zHalf,xRot,yRot,zRot)

    #centres pivot, and cube orientation reset, then moves y pivot down
    cmds.xform(cubeTrans, centerPivots=True)
    cmds.rotate(0,0,0,cubeTrans)

    #Move pivot up or down of centre
    if y == 0: #pivot low, flip onto same height
        cmds.move(0,-0.5,0,'%s.scalePivot' % cubeTrans, '%s.rotatePivot' % cubeTrans, r=True)
    elif y == -1: #pivot low, flip forward and down
        cmds.move(0,-0.5,0,'%s.scalePivot' % cubeTrans, '%s.rotatePivot' % cubeTrans, r=True)
        xRot = xRot*2
        zRot = zRot*2
    else: #pivot high, flip forward and heigh
        cmds.move(0,0.5,0,'%s.scalePivot' % cubeTrans, '%s.rotatePivot' % cubeTrans, r=True)
        xRot = xRot*2
        zRot = zRot*2
    #move pivot x;z (to an edge)
    cmds.move(zHalf,0,xHalf,'%s.scalePivot' % cubeTrans, '%s.rotatePivot' % cubeTrans, r=True)


    cmds.setKeyframe(cubeTrans, time=startTime)
    cmds.rotate(xRot,0,zRot, cubeTrans, r=True)
    cmds.setKeyframe(cubeTrans, time=endTime)


#make cube
deleteExisting('myCube')
cube = cmds.polyCube(name='myCube#')[0]
makePivotKeyable(cube)
cmds.move(0,0.5,0, cube, r=True)

t1 = 0
t2 = 19


for i in range(0,3):
    rollCube([1,0,0],t1,t2, cube)
    t1 += 20
    t2 += 20
