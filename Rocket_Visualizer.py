import bpy
import csv   
import math as m
import os

ops = bpy.ops
data = bpy.data
context = bpy.context
context.scene.animall_properties.key_point_location = True

componentsFile = "reversed_trimmed_components.csv"
decisionFile = "reversed_trimmed_decision_fitness.csv"

componentsFile = os.path.join(os.path.dirname(bpy.data.filepath), componentsFile)
decisionFile = os.path.join(os.path.dirname(bpy.data.filepath), decisionFile)


"'Initialize' a rocket with the part names that will be changed."
with open(decisionFile, newline='') as csv1:
    with open(componentsFile, newline='') as csv2:
        decisionReader = csv.reader(csv1, delimiter = ',')
        componentsReader = csv.reader(csv2, delimiter = ',')
        next(decisionReader, None)
        row = next(componentsReader, None)
        row = next(componentsReader, None)
        vars = next(decisionReader, None)
        "All measurements are in meters"
        root1 = float(vars[6]) *(1/39.3700787)
        tip1 = float(vars[7]) *(1/39.3700787)
        span1 = float(vars[9]) *(1/39.3700787)
        root2 = float(vars[10]) *(1/39.3700787)
        tip2 = float(vars[11]) *(1/39.3700787)
        span2 = float(vars[13]) *(1/39.3700787)
        sweep2 = float(vars[24]) *(1/39.3700787)
        sweep1 = float(vars[25]) *(1/39.3700787)
        diameter2 = float(vars[26]) *(1/39.3700787)
        diameter1 = float(vars[32]) *(1/39.3700787)
        #apogee = -1*float(vars[38]) #Kilometers     maybe for a future graph or something, maybe sit boosters beside it too
        
        "Components Section here, top to bottom"
        motor2 = float(row[3])
        vars = next(componentsReader, None)
        body3 = float(vars[3])
        vars = next(componentsReader, None)
        body2 = float(vars[3])
        vars = next(componentsReader, None)
        transition = float(vars[3])
        vars = next(componentsReader, None)
        coupler = float(vars[3])
        vars = next(componentsReader, None)
        vars = next(componentsReader, None)
        motor1 = float(vars[3])
        vars = next(componentsReader, None)
        body1 = float(vars[3])
        vars = next(componentsReader, None)
        parachute = float(vars[3])
        vars = next(componentsReader, None)
        vars = next(componentsReader, None)
        vars = next(componentsReader, None)
        nose = float(vars[3])
        vars = next(componentsReader, None)
        vars = next(componentsReader, None)

        
"Calculate heights and variables"
noseSections = 15 #Changeable
transitionSections = 15 #Changeable
vertices = 24 #DO NOT EVER CHANGE
wingThickness = .4375 * (1/39.3700387) #meters

wingRadialTranslate1 = (diameter1/2)+(span1/2)
wingRadialTranslate2 = (diameter2/2)+(span2/2)
translate1 = root1-sweep1-tip1
translate2 = root2-sweep2-tip2

    #starting height of fin to match bottom of rocket
finHeight1 = (root1/2)
if translate1<=0:
    finHeight1=(root1/2)-translate1

    #booster height off ground
boostDistOffGround = motor2/2
if translate1 <= 0:
    boostDistOffGround = (motor2/2) - translate1
    
    #sustainer height off ground
sustDistOffGround = (motor1/2)+coupler+transition+body2+body3+motor2
if translate1<=0:
    sustDistOffGround = (motor1/2)+coupler+transition+body2+body3+motor2-translate1

finHeight2 = sustDistOffGround -(motor1/2)+(root2/2)
coneHeight = sustDistOffGround + (motor1/2)+parachute+body1



"Add the rocket pieces in at the right heights and stuff and give names"

"Booster"
ops.mesh.primitive_cylinder_add(vertices=vertices, radius=1/2, depth=1, location= (0,0,boostDistOffGround))
booster = context.active_object
bpy.data.objects['Cylinder'].name = 'booster'
ops.object.shade_smooth(use_auto_smooth=True)

"Fin1"
ops.mesh.primitive_cube_add(size=1, enter_editmode=True, location=(0,-wingRadialTranslate1, finHeight1),scale = (wingThickness, 1, 1))
ops.object.editmode_toggle()
fin1 = context.active_object
data.objects['Cube'].name = 'fin1'

"Fin2"
ops.mesh.primitive_cube_add(size=1, enter_editmode=True, location=(wingRadialTranslate1,0, finHeight1),scale = (1, wingThickness, 1))
fin2 = context.active_object
data.objects['Cube'].name = 'fin2'
ops.object.editmode_toggle()

"Fin3"
ops.mesh.primitive_cube_add(size=1, enter_editmode=True, location=(0, wingRadialTranslate1, finHeight1),scale = (wingThickness, 1, 1))
fin3 = context.active_object
data.objects['Cube'].name = 'fin3'
ops.object.editmode_toggle()

"Fin4"
ops.mesh.primitive_cube_add(size=1, enter_editmode=True, location=(-1*wingRadialTranslate1,0, finHeight1),scale = (1, wingThickness, 1))
fin4 = context.active_object
data.objects['Cube'].name = 'fin4'
ops.object.editmode_toggle()

"body3"
ops.mesh.primitive_cylinder_add(vertices=vertices, radius=1/2, depth=1, location= (0,0,boostDistOffGround+(motor2/2)+(body3/2)))
body3Object = context.active_object
data.objects['Cylinder'].name = 'body3'
ops.object.shade_smooth(use_auto_smooth=True)

"body2"
ops.mesh.primitive_cylinder_add(vertices=vertices, radius=1/2, depth=1, location= (0,0,boostDistOffGround+body3+(motor2/2)+(body2/2)))
body2Object = context.active_object
data.objects['Cylinder'].name = 'body2'
ops.object.shade_smooth(use_auto_smooth=True)

"Transition is with nose cone"

"Coupler"
ops.mesh.primitive_cylinder_add(vertices=vertices, radius=1/2, depth=1, location= (0,0,boostDistOffGround+(motor2/2)+body3+body2+transition+(coupler/2)))
couplerObject = context.active_object
data.objects['Cylinder'].name = 'coupler'
ops.object.shade_smooth(use_auto_smooth=True)

"Sustainer"
ops.mesh.primitive_cylinder_add(vertices=vertices, radius=1/2, depth=1, location= (0,0,sustDistOffGround))
sustainer = context.active_object
data.objects['Cylinder'].name = 'sustainer'
ops.object.shade_smooth(use_auto_smooth=True)

"fin5"
ops.mesh.primitive_cube_add(size=1, enter_editmode=True, location=(0,-wingRadialTranslate2, finHeight2),scale = (wingThickness, 1, 1))
fin5 = context.active_object
data.objects['Cube'].name = 'fin5'
ops.object.editmode_toggle()

"fin6"
ops.mesh.primitive_cube_add(size=1, enter_editmode=True, location=(wingRadialTranslate2,0, finHeight2),scale = (1, wingThickness, 1))
fin6 = context.active_object
data.objects['Cube'].name = 'fin6'
ops.object.editmode_toggle()

"fin7"
ops.mesh.primitive_cube_add(size=1, enter_editmode=True, location=(0,wingRadialTranslate2, finHeight2),scale = (wingThickness, 1, 1))
fin7 = context.active_object
data.objects['Cube'].name = 'fin7'
ops.object.editmode_toggle()

"fin8"
ops.mesh.primitive_cube_add(size=1, enter_editmode=True, location=(-wingRadialTranslate2,0, finHeight2),scale = (1, wingThickness, 1))
fin6 = context.active_object
data.objects['Cube'].name = 'fin8'
ops.object.editmode_toggle()

"body1"
ops.mesh.primitive_cylinder_add(vertices=vertices, radius=1/2, depth=1, location= (0,0,sustDistOffGround+(motor1/2)+(body1/2)))
body1Object = context.active_object
data.objects['Cylinder'].name = 'body1'
ops.object.shade_smooth(use_auto_smooth=True)

"parachute"
ops.mesh.primitive_cylinder_add(vertices=vertices, radius=1/2, depth=1, location= (0,0,sustDistOffGround+(motor1/2)+body1+(parachute/2)))
parachuteObject = context.active_object
data.objects['Cylinder'].name = 'parachute'
ops.object.shade_smooth(use_auto_smooth=True)


"Von Karman Function"
def y(x, L, diam):
    inside = 1-((2*x)/L)
    theta = m.acos(inside)
    coeff = (diam)/(2*m.sqrt(m.pi))
    return coeff * m.sqrt(theta - ((m.sin(2*theta))/2))

"nose"
j=1
while j <= noseSections:
    deltaX=nose/noseSections
    radius2=.5#top
    radius1=.5#bottom
    ops.mesh.primitive_cone_add(vertices=vertices, radius1= radius1, radius2=radius2, depth = deltaX,enter_editmode=False, align='WORLD',location=(0,0,((deltaX/2)-(deltaX*(j-noseSections))+coneHeight)),scale=(1, 1, 1))
    data.objects['Cone'].name = 'nose'+ str(j)
    ops.object.shade_smooth(use_auto_smooth=True)
    j+=1

"transition"
j=1
while j <= transitionSections:
    deltaX = transition/transitionSections
    radius2 = .5#top
    radius1 = .5#bottom
    ops.mesh.primitive_cone_add(vertices = vertices, radius1= radius1, radius2 = radius2, depth= deltaX, enter_editmode=False, align='WORLD', location=(0, 0, ((deltaX/2)-(deltaX*(j-transitionSections)) + boostDistOffGround + (motor2/2) + body3 + body2)), scale=(1, 1, 1))
    data.objects['Cone'].name = 'transition'+str(j)
    ops.object.shade_smooth(use_auto_smooth=True)
    j+=1


"---------------------------------Change pieces and add keystones-------------------------------------"

"select time, select object, move and scale it, add move and scale keyframe"
frame = 1
with open(decisionFile, newline='') as csv1:
    with open(componentsFile, newline='') as csv2:
        decisionReader = csv.reader(csv1, delimiter = ',')
        componentsReader = csv.reader(csv2, delimiter = ',')
        vars = next(decisionReader, None)
        row = next(componentsReader, None)
        
        for decision in decisionReader:
            "select time according to 'iterations'"
            

            "Grab all the data"
            fit = (decision[1])
            # "All measurements are in meters now"
            root1 = float(decision[6]) *(1/39.3700787)
            tip1 = float(decision[7]) *(1/39.3700787)
            span1 = float(decision[9]) *(1/39.3700787)
            root2 = float(decision[10]) *(1/39.3700787)
            tip2 = float(decision[11]) *(1/39.3700787)
            span2 = float(decision[13]) *(1/39.3700787)
            sweep2 = float(decision[24]) *(1/39.3700787)
            sweep1 = float(decision[25]) *(1/39.3700787)
            diameter2 = float(decision[26]) *(1/39.3700787)
            diameter1 = float(decision[32]) *(1/39.3700787)
            

            "Grab all the data"
            row = next(componentsReader, None)
            motor2 = float(row[3])
            row = next(componentsReader, None)
            body3 = float(row[3])
            row = next(componentsReader, None)
            body2 = float(row[3])
            row = next(componentsReader, None)
            transition = float(row[3])
            row = next(componentsReader, None)
            coupler = float(row[3])
            row = next(componentsReader, None)
            row = next(componentsReader, None)
            motor1 = float(row[3])
            row = next(componentsReader, None)
            body1 = float(row[3])
            row = next(componentsReader, None)
            parachute = float(row[3])
            row = next(componentsReader, None)
            row = next(componentsReader, None)
            row = next(componentsReader, None)
            nose = float(row[3])
            row = next(componentsReader, None)
            # row = next(componentsReader, None)
            # row = next(componentsReader, None)
            
            if (fit == "True"):
                context.scene.frame_current = frame
                "Recalculate the variables"
                wingRadialTranslate1 = (diameter1/2)+(span1/2)
                wingRadialTranslate2 = (diameter2/2)+(span2/2)
                translate1 = root1-(sweep1+tip1)
                translate2 = root2-(sweep2+tip2)

                    #starting height of fin to match bottom of rocket
                finHeight1 = (root1/2)
                if translate1<=0:
                    finHeight1=(root1/2)-translate1

                    #booster height off ground
                boostDistOffGround = motor2/2
                if translate1 <= 0:
                    boostDistOffGround = (motor2/2) - translate1
                    
                    #sustainer height off ground
                sustDistOffGround = (motor1/2)+coupler+transition+body2+body3+motor2
                if translate1<=0:
                    sustDistOffGround = (motor1/2)+coupler+transition+body2+body3+motor2-translate1

                finHeight2 = sustDistOffGround -(motor1/2)+(root2/2)
                coneHeight = sustDistOffGround + (motor1/2)+parachute+body1
                

                "Booster"
                object = context.scene.objects['booster']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,0,boostDistOffGround)
                context.active_object.scale = (diameter1,diameter1,motor2)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                
                "body3"
                object = context.scene.objects['body3']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,0,boostDistOffGround+(motor2/2)+(body3/2))
                context.active_object.scale = (diameter1,diameter1,body3)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')

                "body2"
                object = context.scene.objects['body2']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,0,boostDistOffGround+(motor2/2)+(body2/2)+body3)
                context.active_object.scale = (diameter1,diameter1,body2)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')

                "coupler"
                object = context.scene.objects['coupler']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,0,boostDistOffGround+(motor2/2)+body3+body2+transition+(coupler/2))
                context.active_object.scale = (diameter2,diameter2,coupler)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')

                "sustainer"
                object = context.scene.objects['sustainer']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,0,sustDistOffGround)
                context.active_object.scale = (diameter2,diameter2,motor1)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')

                "body1"
                object = context.scene.objects['body1']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,0,sustDistOffGround+(motor1/2)+(body1/2))
                context.active_object.scale = (diameter2,diameter2,body1)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')

                "parachute"
                object = context.scene.objects['parachute']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,0,sustDistOffGround+(motor1/2)+body1+(parachute/2))
                context.active_object.scale = (diameter2,diameter2,parachute)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                if frame == 1:
                    prevTrans1 = 0
                    prevSweep1 = 0
                    prevTrans2 = 0
                    prevSweep2 = 0
              
                "Wing vertices need to be moved back to starting position before moving to the normal position"
                "fin1"
                object = context.scene.objects['fin1']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,-wingRadialTranslate1,finHeight1)
                context.active_object.scale = (1,span1,root1)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                ops.object.editmode_toggle()
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 2, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 10, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 3, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 6, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 2, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 10, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 3, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 6, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.editmode_toggle()
                ops.anim.insert_keyframe_animall()
                

                "fin2"
                object = context.scene.objects['fin2']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (wingRadialTranslate1,0,finHeight1)
                context.active_object.scale = (span1,1,root1)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                ops.object.editmode_toggle()
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 4, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 2, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 3, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 5, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 4, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 2, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 3, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 5, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.editmode_toggle()
                ops.anim.insert_keyframe_animall()
                
                
                

                "fin3"
                object = context.scene.objects['fin3']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,wingRadialTranslate1,finHeight1)
                context.active_object.scale = (1,span1,root1)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                ops.object.editmode_toggle()
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 4, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 15, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 1, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 5, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 4, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 15, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 1, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 5, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.editmode_toggle()
                ops.anim.insert_keyframe_animall()
             

                "fin4"
                object = context.scene.objects['fin4']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (-wingRadialTranslate1,0,finHeight1)
                context.active_object.scale = (span1,1,root1)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                ops.object.editmode_toggle()
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 10, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 15, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 1, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 0, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 10, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 15, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 1, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 0, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.editmode_toggle()
                ops.anim.insert_keyframe_animall()

                "fin5"
                object = context.scene.objects['fin5']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,-wingRadialTranslate2,finHeight2)
                context.active_object.scale = (1,span2,root2)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                ops.object.editmode_toggle()
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 2, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 10, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 3, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 6, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 2, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 10, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 3, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 6, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.editmode_toggle()
                ops.anim.insert_keyframe_animall()
                

                "fin6"
                object = context.scene.objects['fin6']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (wingRadialTranslate2,0,finHeight2)
                context.active_object.scale = (span2,1,root2)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                ops.object.editmode_toggle()
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 4, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 2, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 3, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 5, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 4, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 2, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 3, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 5, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.editmode_toggle()
                ops.anim.insert_keyframe_animall()
                
                
                

                "fin7"
                object = context.scene.objects['fin7']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (0,wingRadialTranslate2,finHeight2)
                context.active_object.scale = (1,span2,root2)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                ops.object.editmode_toggle()
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 4, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 15, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 1, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 5, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 4, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 15, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 1, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 5, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.editmode_toggle()
                ops.anim.insert_keyframe_animall()
             

                "fin8"
                object = context.scene.objects['fin8']
                ops.object.select_all(action='DESELECT')
                object.select_set(True)
                context.view_layer.objects.active = object
                context.active_object.location = (-wingRadialTranslate2,0,finHeight2)
                context.active_object.scale = (span2,1,root2)
                context.active_object.keyframe_insert(data_path='location')
                context.active_object.keyframe_insert(data_path='scale')
                ops.object.editmode_toggle()
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 10, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 15, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, prevSweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 1, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 0, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -prevTrans2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio=(1/8), seed = 10, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 15, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, -sweep2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 1, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                ops.mesh.select_random(ratio = (1/8), seed = 0, action='SELECT')
                bpy.ops.transform.translate(value=(-0, -0, translate2), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.editmode_toggle()
                ops.anim.insert_keyframe_animall()
                
                prevTrans1 = translate1
                prevSweep1 = sweep1
                prevTrans2 = translate2
                prevSweep2 = sweep2




                "Reset vertice back to start, rotate cone by 2*pi/24, repeat. Then move vertice to normal position, rotate by 2*pi/24, repeat."
                masterList = [19,55,17,36,38,28,27,99,35,22,3,59,57,15,16,40,2,86,88,11,4,37,75,18]
                inverseMasterList = [106,21,37,10,12,0,73,34,28,48,36,1,17,206,2,35,124,4,54,22,154,64,19,86]
                "nose"
                j=1
                deltaXn=nose/noseSections
                while j <= noseSections:    
                    ops.object.select_all(action='DESELECT')
                    noseName = 'nose'+str(j)
                    object = context.scene.objects[noseName]
                    context.view_layer.objects.active = object
                    object.select_set(True)
                    context.active_object.location = (0, 0, (coneHeight+(deltaXn/2)+(deltaXn*(noseSections-j))))
                    context.active_object.keyframe_insert(data_path='location')
                    i = 1
                    if (frame == 1):
                        radius2 = .5- y(deltaXn*(j-1),6*diameter2, diameter2)#top
                        radius1 = .5- y(deltaXn*j,6*diameter2, diameter2)#bottom
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (1/(vertices*2)), seed = masterList[(i-1)], action = 'SELECT')
                            ops.transform.translate(value=(-radius2, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            object.select_set(True)
                            ops.transform.rotate(value=-(2*m.pi)/24, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            i+=1
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (47/(vertices*2)), seed = inverseMasterList[(i-1)], action = 'SELECT')
                            ops.mesh.select_all(action='INVERT') #had to do this instead cause there was a missing vertex with just random selection. Selected everything else except that one then inverted the selection
                            ops.transform.translate(value=(radius1, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            object.select_set(True)
                            ops.transform.rotate(value=(2*m.pi)/24, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            i+=1
                        ops.object.editmode_toggle()
                        ops.anim.insert_keyframe_animall()
                        ops.object.editmode_toggle()
                        
                    else:
                        prevradius2 =  .5- y(oldDeltaXn*(j-1),6*oldDiameter2, oldDiameter2)#top
                        prevradius1 = .5- y(oldDeltaXn*(j),6*oldDiameter2, oldDiameter2)#bottom
                        radius2 = .5- y(deltaXn*(j-1),6*diameter2, diameter2)#top
                        radius1 = .5- y(deltaXn*j,6*diameter2, diameter2)#bottom
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (1/(vertices*2)), seed = masterList[(i-1)], action = 'SELECT')
                            ops.transform.translate(value=(prevradius2, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            object.select_set(True)
                            ops.transform.rotate(value=-(2*m.pi)/24, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            i+=1
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (47/(vertices*2)), seed = inverseMasterList[(i-1)], action = 'SELECT')
                            ops.mesh.select_all(action='INVERT') #had to do this instead cause there was a missing vertex with just random selection. Selected everything else except that one then inverted the selection
                            ops.transform.translate(value=(-prevradius1, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            object.select_set(True)
                            ops.transform.rotate(value=(2*m.pi)/24, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            i+=1
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (1/(vertices*2)), seed = masterList[(i-1)], action = 'SELECT')
                            ops.transform.translate(value=(-radius2, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            object.select_set(True)
                            ops.transform.rotate(value=-(2*m.pi)/24, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            i+=1
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (47/(vertices*2)), seed = inverseMasterList[(i-1)], action = 'SELECT')
                            ops.mesh.select_all(action='INVERT') #had to do this instead cause there was a missing vertex with just random selection. Selected everything else except that one then inverted the selection
                            ops.transform.translate(value=(radius1, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            object.select_set(True)
                            ops.transform.rotate(value=(2*m.pi)/24, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            i+=1
                        ops.object.editmode_toggle()
                        ops.anim.insert_keyframe_animall()
                        ops.object.editmode_toggle()
                    oldDeltaXn = deltaXn
                    j+=1
                
                "transition"
                j=1
                while j <= transitionSections:
                    deltaXt = transition/transitionSections
                    ops.object.select_all(action='DESELECT')
                    noseName = 'transition'+str(j)
                    object = context.scene.objects[noseName]
                    context.view_layer.objects.active = object
                    object.select_set(True)
                    context.active_object.location = (0, 0, ((deltaXt/2)-(deltaXt*(j-transitionSections)) + boostDistOffGround + (motor2/2) + body3 + body2))
                    context.active_object.keyframe_insert(data_path='location')
                    i = 1
                    if (frame == 1):
                        radius2 = .5-y(((deltaXt*(j-1))+((6*diameter1)-(transition))),6*diameter1, diameter1)#top
                        radius1 = .5-y((deltaXt*j)+(6*diameter1-transition),6*diameter1, diameter1)#bottom
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (1/(vertices*2)), seed = masterList[(i-1)], action = 'SELECT')
                            ops.transform.translate(value=(-radius2, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            ops.transform.rotate(value=(2*m.pi)/24, orient_axis='Z')
                            i+=1
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (47/(vertices*2)), seed = inverseMasterList[(i-1)], action = 'SELECT')
                            ops.mesh.select_all(action='INVERT') #had to do this instead cause there was a missing vertex with just random selection. Selected everything else except that one then inverted the selection
                            ops.transform.translate(value=(radius1, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            ops.transform.rotate(value=-(2*m.pi)/24, orient_axis='Z')
                            i+=1
                        ops.object.editmode_toggle()
                        ops.anim.insert_keyframe_animall()
                        ops.object.editmode_toggle()
                    else:
                        prevradius2 = .5 - y((oldDeltaXt*(j-1))+((6*oldDiameter1)-(oldTransition)), (6*oldDiameter1), oldDiameter1)
                        prevradius1 = .5 - y((oldDeltaXt*(j))+((6*oldDiameter1)-(oldTransition)), (6*oldDiameter1), oldDiameter1)
                        radius2 = .5-y(((deltaXt*(j-1))+((6*diameter1)-(transition))),6*diameter1, diameter1)#top
                        radius1 = .5-y((deltaXt*j)+(6*diameter1-transition),6*diameter1, diameter1)#bottom
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (1/(vertices*2)), seed = masterList[(i-1)], action = 'SELECT')
                            ops.transform.translate(value=(prevradius2, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            object.select_set(True)
                            ops.transform.rotate(value=-(2*m.pi)/24, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            i+=1
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (47/(vertices*2)), seed = inverseMasterList[(i-1)], action = 'SELECT')
                            ops.mesh.select_all(action='INVERT') #had to do this instead cause there was a missing vertex with just random selection. Selected everything else except that one then inverted the selection
                            ops.transform.translate(value=(-prevradius1, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            object.select_set(True)
                            ops.transform.rotate(value=(2*m.pi)/24, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            i+=1
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (1/(vertices*2)), seed = masterList[(i-1)], action = 'SELECT')
                            ops.transform.translate(value=(-radius2, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            ops.transform.rotate(value=(2*m.pi)/24, orient_axis='Z')
                            i+=1
                        i = 1
                        while i<= vertices:
                            ops.object.editmode_toggle()
                            ops.mesh.select_all(action='DESELECT')
                            ops.mesh.select_random(ratio = (47/(vertices*2)), seed = inverseMasterList[(i-1)], action = 'SELECT')
                            ops.mesh.select_all(action='INVERT') #had to do this instead cause there was a missing vertex with just random selection. Selected everything else except that one then inverted the selection
                            ops.transform.translate(value=(radius1, -0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False, release_confirm=True)
                            ops.object.editmode_toggle()
                            ops.transform.rotate(value=-(2*m.pi)/24, orient_axis='Z')
                            i+=1
                        ops.object.editmode_toggle()
                        ops.anim.insert_keyframe_animall()
                        ops.object.editmode_toggle()
                    oldDiameter1 = diameter1
                    oldDiameter2 = diameter2
                    oldTransition = transition
                    oldDeltaXt = deltaXt
                    j+=1
                frame = frame + 1
                if ((frame % 10) == 0):
                    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath) #Save file every 10 rockets printed
            "end"
"Thats it"

            
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath) #save the file once finished. 