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

#edit

def rollCube(vect, startTime, endTime, cubeTrans):
    x,y,z = vect
    xRot,yRot,zRot = x*90, y*90, z*(-90)
    xHalf, yHalf, zHalf = x*0.5, y*0.5, z*0.5
    print(x,y,z,xHalf,yHalf,zHalf,xRot,yRot,zRot)
    #centres pivot, then moves y pivot down, then in x/z directions
    cmds.xform(cubeTrans, centerPivots=True)
    cmds.rotate(0,0,0,cubeTrans)
    cmds.move(0,-0.5,0,'myCube1.scalePivot', 'myCube1.rotatePivot', r=True)
    cmds.move(zHalf,0,xHalf,'myCube1.scalePivot', 'myCube1.rotatePivot', r=True)

    #
    cmds.setKeyframe(cubeTrans, time=startTime)
    cmds.rotate(xRot,0,zRot, cubeTrans, r=True)

    cmds.setKeyframe(cubeTrans, time=endTime)
    #
    # #cube has moved, z-=1, so move the pivot accordingly
    # cmds.move(0,0,-1,'myCube1.scalePivot', 'myCube1.rotatePivot', r=True)
    # cmds.setKeyframe(cube, time=21)
    # cmds.rotate(-90,0,0, cube, r=True)
    # cmds.setKeyframe(cube, time=42)
    # cmds.xform(cubeTrans, centerPivots=True)

t1 = 0
t2 = 19
for i in range(0,3):
    rollCube([0,0,1],t1,t2, cube)
    t1 += 20
    t2 += 20
    rollCube([1,0,0],t1,t2, cube)
    t1 += 20
    t2 += 20

for i in range(0,4):
    rollCube([-1,0,0],t1,t2,cube)
    t1 +=20
    t2 +=20
for i in range(0,4):
    rollCube([0,0,-1],t1,t2, cube)
    t1 += 20
    t2 += 20
