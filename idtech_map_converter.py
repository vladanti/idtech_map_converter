# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 19:41:23 2024

@author: Vlad
"""

import os

# convert constants for scale 0.0260053
scaleFactor = 0.0234375
scaleTex = 1 / scaleFactor

# open idTech 4 map file
idtech4map = open("C://Users/Vlad/Documents/id Software/idStudio/doom-mod-1881605139/base/maps/mars_city1.map", "r")

# create empty map idTech 7 file
idtech7map = open("C://Users/Vlad/Documents/id Software/idStudio/doom-mod-1881605139/base/maps/mars_city1_test_2.map", "w")

# write header of idtech7 map
idtech7map.write("Version 7\nHierarchyVersion 1\nentity {\n\tentityDef world {\n\t\tinherit = \"worldspawn\";\n\t\tedit = {\n\t\t}\n\t}\n")

# read the content of the file opened 
mapcontent = idtech4map.readlines()

def brushconvert(brushface_list):
    #flag var for passing unusable legacy brushes like visportals
    #passflag = 0
    
    x = brushface_list[1]
    y = brushface_list[2]
    z = brushface_list[3]
    
    dist = float(brushface_list[4]) * scaleFactor
    #print(brushface_list[4], "*", scaleFactor, "=", dist)
    
    xxscale = float(brushface_list[8]) * scaleTex
    xyscale = float(brushface_list[9]) * scaleTex
    xoffset = float(brushface_list[10]) * scaleTex
    yxscale = float(brushface_list[13]) * scaleTex
    yyscale = float(brushface_list[14]) * scaleTex
    yoffset = float(brushface_list[15]) * scaleTex
    
    material = brushface_list[18]
    
    a = brushface_list[19]
    b = brushface_list[20]
    c = brushface_list[21]
    
    # update service materials
    if material == "\"textures/common/clip\"":
        material = "\"art/tile/common/clip/clip\""
    elif material == "\"textures/common/caulk\"":
        material = "\"art/tile/common/caulk\""
    elif material == "\"textures/common/monster_clip\"":
        material = "\"art/tile/common/clip/clip_monster\""
    elif material == "\"textures/common/nodraw\"":
        material = "\"art/tile/common/nodraw\""
    elif material == "\"textures/common/trigonce\"":
        material = "\"editor/worldeditor/trigger\""
    elif material == "\"textures/common/player_clip\"":
        material = "\"art/tile/common/clip/clip_player\""
    elif material == "\"textures/common/moveable_clip\"":
        material = "\"art/tile/common/clip/clip\""
    #------------------------------------------------------- 
    elif material == "\"textures/base_floor/sflgrate2\"":
        material = "\"art/tile/uac/floor/grate_floor_tile_01\""
    elif material == "\"textures/mcity/mchangar2\"":
        material = "\"art/tile/uac/floor/diamondplate_a_rt\""
    # if not service then create mat
    else:
        # check for material existance
        clear_path = (material[1:-1])
        material_path = "C://Users/Vlad/Documents/id Software/idStudio/doom-mod-1881605139/base/declTree/material2/" + clear_path + ".decl"
        if not os.path.isfile(material_path):
            devider = "/"
            dir_path = "C://Users/Vlad/Documents/id Software/idStudio/doom-mod-1881605139/base/declTree/material2/" +  devider.join(((material[1:-1]).split('/'))[:-1])
            print(dir_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            #materialName = ((material[1:-1]).split('/'))[-1]
            materialFile = open(material_path, "w")
            materialFile.write("declType( material2 ) {\n\tinherit = \"template/pbr\";\n\tedit = {\n\t\tRenderLayers = {\n\t\t\titem[0] = {\n\t\t\t\tparms = {\n\t\t\t\t\tnormal = {\n\t\t\t\t\t\tfilePath = \"" + clear_path + "_local.tga\";\n\t\t\t\t\t}\n\t\t\t\t\t\tspecular = {\n\t\t\t\t\t\tfilePath = \"" + clear_path + "_s.tga\";\n\t\t\t\t\t}\n\t\t\t\t\talbedo = {\n\t\t\t\t\t\tfilePath = \"" + clear_path + ".tga\";\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}")
    
    idtech7_brushface = "( "+x+" "+y+" "+z+" "+str(dist)+" ) ( ( "+str(xxscale)+" "+str(xyscale)+" "+str(xoffset)+" ) ( "+str(yxscale)+" "+str(yyscale)+" "+str(yoffset)+" ) ) " + material + " " + a + " " + b + " " + c
    
    return idtech7_brushface
    #check should we pass brush or return it
    # if (passflag == 0):
    #     return idtech7_brushface
    # elif (passflag == 0):
    #     return ""

#------------------------------------------------
# parse idTech 4 map brushes
#------------------------------------------------

linecount = 0

for line in mapcontent:
    
    # brush entity parse and write
    if "brushDef3" in line:
        
        # visportal brushes remover
        # if "textures/editor/visportal" in mapcontent[(linecount + 2)]:
        #     continue
        # elif "textures/editor/visportal" in mapcontent[(linecount + 3)]:
        #     continue
        # elif "textures/editor/visportal" in mapcontent[(linecount + 4)]:
        #     continue
        # elif "textures/editor/visportal" in mapcontent[(linecount + 5)]:
        #     continue
        # elif "textures/editor/visportal" in mapcontent[(linecount + 6)]:
        #     continue
        # elif "textures/editor/visportal" in mapcontent[(linecount + 7)]:
        #     continue
        
        # write brush header
        idtech7map.write("{\n\tbrushDef3 {\n")
        
        # set counter to 1
        count = 2
        
        # until we have planes
        while ("}" not in mapcontent[(linecount + count)]):
            
            # recalc plane for brush
            brushface_recalc = brushconvert((mapcontent[(linecount + count)]).split())
            
            # write brush header
            idtech7map.write("\t\t" + brushface_recalc + "\n")
            
            # brush plane counter
            count = count + 1
            
        # close brush structure with }
        idtech7map.write("\t}\n}\n")
        
    
    # increment line counter
    linecount = linecount + 1

# close geometry entity
idtech7map.write("}\n")

#------------------------------------------------
# parse idTech 4 map lights
#------------------------------------------------

# set line counter to 0 again
linecount = 0

# lights need ids
lightcount = 1

for line in mapcontent:
    
    # light entity parse and write
    if "\"classname\" \"light\"" in line:
        
        # write light entity header
        idtech7map.write("entity {\n\tgroups {\n\t\t\"lights\"\n\t}\n\tentityDef light_" + str(lightcount) + " {\n\t\tinherit = \"light\";\n\t\tedit = {\n")
        
        # set counter to 1
        count = 1
        
        # until we have light properies
        while ("}" not in mapcontent[(linecount + count)]):
            
            # current line
            current_line = mapcontent[(linecount + count)]
            
            # search for known idTech 4 properties
            if "origin" in current_line:
                # parse coordinates
                originX = float(((current_line.split())[1])[1:]) * scaleFactor
                originY = float((current_line.split())[2]) * scaleFactor
                originZ = float(((current_line.split())[3])[:-1]) * scaleFactor
                #print(originX, originY, originZ)
                idtech7map.write("\t\t\tspawnPosition = {\n\t\t\t\tx = " + str(originX) + ";\n\t\t\t\ty = " + str(originY) + ";\n\t\t\t\tz = " + str(originZ) + ";\n\t\t\t}\n")
            elif "_color" in mapcontent[(linecount + count)]:
                # parse coordinates
                R = ((current_line.split())[1])[1:]
                G = (current_line.split())[2]
                B = ((current_line.split())[3])[:-1]
                #print(R, G, B)
                idtech7map.write("\t\t\tlightColor = {\n\t\t\t\tr = " + R + ";\n\t\t\t\tg = " + G + ";\n\t\t\t\tb = " + B + ";\n\t\t\t}\n")
            elif "light_radius" in current_line:
                # parse coordinates
                raduisX = float(((current_line.split())[1])[1:]) * scaleFactor
                raduisY = float((current_line.split())[2]) * scaleFactor
                raduisZ = float(((current_line.split())[3])[:-1]) * scaleFactor
                #print(raduisX, raduisY, raduisZ)
                idtech7map.write("\t\t\tlightRadius = {\n\t\t\t\tx = " + str(raduisX) + ";\n\t\t\t\ty = " + str(raduisY) + ";\n\t\t\t\tz = " + str(raduisZ) + ";\n\t\t\t}\n")
            elif "light_center" in current_line:
                # parse coordinates
                centerX = float(((current_line.split())[1])[1:]) * scaleFactor
                centerY = float((current_line.split())[2]) * scaleFactor
                centerZ = float(((current_line.split())[3])[:-1]) * scaleFactor
                #print(raduisX, raduisY, raduisZ)
                idtech7map.write("\t\t\tlightCenter = {\n\t\t\t\tx = " + str(centerX) + ";\n\t\t\t\ty = " + str(centerY) + ";\n\t\t\t\tz = " + str(centerZ) + ";\n\t\t\t}\n")
            
            # light properties lines counter
            count = count + 1
            
            lightcount = lightcount + 1
            
        # close light structure with }
        idtech7map.write("\t\t}\n\t}\n}\n")
        
    
    # increment line counter
    linecount = linecount + 1
    
#------------------------------------------------
# parse idTech 4 map static meshes
#------------------------------------------------

# set line counter to 0 again
linecount = 0

# static also need ids
staticCount = 1

for line in mapcontent:
    
    # static entity parse and write
    if "\"classname\" \"func_static\"" in line:
        
        # write static entity header
        idtech7map.write("entity {\n\tgroups {\n\t\t\"static_meshes\"\n\t}\n\tentityDef func_static_" + str(staticCount) + " {\n\t\tinherit = \"func/static\";\n\t\tedit = {\n")
        
        # set counter to 1
        count = 1
        
        # until we have sraric properies
        while ("}" not in mapcontent[(linecount + count)]):
            
            # current line
            current_line = mapcontent[(linecount + count)]
            
            # search for known idTech 4 properties
            if "origin" in current_line:
                # parse coordinates
                originX = float(((current_line.split())[1])[1:]) * scaleFactor
                originY = float((current_line.split())[2]) * scaleFactor
                originZ = float(((current_line.split())[3])[:-1]) * scaleFactor
                #print(originX, originY, originZ)
                idtech7map.write("\t\t\tspawnPosition = {\n\t\t\t\tx = " + str(originX) + ";\n\t\t\t\ty = " + str(originY) + ";\n\t\t\t\tz = " + str(originZ) + ";\n\t\t\t}\n")
            elif "rotation" in current_line:
                # parse rotation coordinates
                mat0X = float(((current_line.split())[1])[1:]) #* scaleFactor
                mat0Y = float((current_line.split())[2]) #* scaleFactor
                mat0Z = float((current_line.split())[3]) #* scaleFactor
                mat1X = float((current_line.split())[4]) #* scaleFactor
                mat1Y = float((current_line.split())[5]) #* scaleFactor
                mat1Z = float((current_line.split())[6]) #* scaleFactor
                mat2X = float((current_line.split())[7]) #* scaleFactor
                mat2Y = float((current_line.split())[8]) #* scaleFactor
                mat2Z = float(((current_line.split())[9])[:-1]) #* scaleFactor
                #print(originX, originY, originZ)
                idtech7map.write("\t\t\tspawnOrientation = {\n\t\t\t\tmat = {\n\t\t\t\t\tmat[0] = {\n\t\t\t\t\t\tx = " + str(mat0X) + ";\n\t\t\t\t\t\ty = " + str(mat0Y) + ";\n\t\t\t\t\t\tz = " + str(mat0Z) + ";\n\t\t\t\t\t}\n\t\t\t\t\tmat[1] = {\n\t\t\t\t\t\tx = " + str(mat1X) + ";\n\t\t\t\t\t\ty = " + str(mat1Y) + ";\n\t\t\t\t\t\tz = " + str(mat1Z) + ";\n\t\t\t\t\t}\n\t\t\t\t\tmat[2] = {\n\t\t\t\t\t\tx = " + str(mat2X) + ";\n\t\t\t\t\t\ty = " + str(mat2Y) + ";\n\t\t\t\t\t\tz = " + str(mat2Z) + ";\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n")
            elif "\"model\"" in mapcontent[(linecount + count)]:
                # parse model path
                modelPath = (current_line.split())[1]
                #modelPath = '"art/breakable/barrel/uac_tech_red_breakable.lwo"'
                #print(modelPath)
                idtech7map.write("\t\t\trenderModelInfo = {\n\t\t\t\tmodel = " + modelPath + ";\n\t\t\t\tscale = {\n\t\t\t\t\tx = " + str(scaleFactor) + ";\n\t\t\t\t\ty = " + str(scaleFactor) + ";\n\t\t\t\t\tz = " + str(scaleFactor) + ";\n\t\t\t\t}\t\t\t}\n")
            
            # static properties lines counter
            count = count + 1
            
            staticCount = staticCount + 1
            
        # close light structure with }
        idtech7map.write("\t\t}\n\t}\n}\n")
        
    
    # increment line counter
    linecount = linecount + 1
    
    
#------------------------------------------------
# parse idTech 4 movable meshes
#------------------------------------------------

# set line counter to 0 again
linecount = 0

# static also need ids
moveableCount = 1

for line in mapcontent:
    
    # static entity parse and write
    if "\"classname\" \"moveable_" in line:
        
        # write static entity header
        idtech7map.write("entity {\n\tgroups {\n\t\t\"prop_moveable\"\n\t}\n\tentityDef prop_moveable_" + str(moveableCount) + " {\n\t\tinherit = \"prop/moveable/havoktest\";\n\t\tedit = {\n")
        
        # set counter to 1
        count = 1
        
        #moveable model replace asset
        if "cone" in line:
            moveableModel = "\"art/kit/uac/prop/cone_caution.lwo\""
        elif "diamondbox" in line:
            moveableModel = "\"art/kit/uac/machine/greeble_box_01.lwo\""
        elif "foamcup" in line:
            moveableModel = "\"art/kit/uac/prop/cup_var_a.lwo\""
        elif "cokecan" in line:
            moveableModel = "\"art/kit/hell_earth/prop/can_beer_01.lwo\""
        elif "chair2" in line:
            moveableModel = "\"art/kit/uac/prop/office_chair_01.lwo\""
        elif "kitchenchair" in line:
            moveableModel = "\"art/kit/uac/prop/breakchair.lwo\""
        else:
            moveableModel = "\"art/kit/uac/prop/cone_caution.lwo\""
        
        
        # until we have moveable properies
        while ("}" not in mapcontent[(linecount + count)]):
            
            # current line
            current_line = mapcontent[(linecount + count)]
            
            # search for known idTech 4 properties
            if "origin" in current_line:
                # parse coordinates
                originX = float(((current_line.split())[1])[1:]) * scaleFactor
                originY = float((current_line.split())[2]) * scaleFactor
                originZ = float(((current_line.split())[3])[:-1]) * scaleFactor
                #print(originX, originY, originZ)
                idtech7map.write("\t\t\tspawnPosition = {\n\t\t\t\tx = " + str(originX) + ";\n\t\t\t\ty = " + str(originY) + ";\n\t\t\t\tz = " + str(originZ) + ";\n\t\t\t}\n")
            elif "rotation" in current_line:
                # parse rotation coordinates
                mat0X = float(((current_line.split())[1])[1:]) #* scaleFactor
                mat0Y = float((current_line.split())[2]) #* scaleFactor
                mat0Z = float((current_line.split())[3]) #* scaleFactor
                mat1X = float((current_line.split())[4]) #* scaleFactor
                mat1Y = float((current_line.split())[5]) #* scaleFactor
                mat1Z = float((current_line.split())[6]) #* scaleFactor
                mat2X = float((current_line.split())[7]) #* scaleFactor
                mat2Y = float((current_line.split())[8]) #* scaleFactor
                mat2Z = float(((current_line.split())[9])[:-1]) #* scaleFactor
                #print(originX, originY, originZ)
                idtech7map.write("\t\t\tspawnOrientation = {\n\t\t\t\tmat = {\n\t\t\t\t\tmat[0] = {\n\t\t\t\t\t\tx = " + str(mat0X) + ";\n\t\t\t\t\t\ty = " + str(mat0Y) + ";\n\t\t\t\t\t\tz = " + str(mat0Z) + ";\n\t\t\t\t\t}\n\t\t\t\t\tmat[1] = {\n\t\t\t\t\t\tx = " + str(mat1X) + ";\n\t\t\t\t\t\ty = " + str(mat1Y) + ";\n\t\t\t\t\t\tz = " + str(mat1Z) + ";\n\t\t\t\t\t}\n\t\t\t\t\tmat[2] = {\n\t\t\t\t\t\tx = " + str(mat2X) + ";\n\t\t\t\t\t\ty = " + str(mat2Y) + ";\n\t\t\t\t\t\tz = " + str(mat2Z) + ";\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n")
                idtech7map.write("\t\t\tremoveFlag = \"RMV_NEVER\";\n\t\t\tflags = {\n\t\t\t\tcanBecomeDormant = false;\n\t\t\t\tnoknockback = true;\n\t\t\t\ttakedamage = false;\n\t\t\t}\n\t\t\trenderModelInfo = {\n\t\t\t\tmodel = " + moveableModel + ";\n\t\t\t}\n\t\t\tclipModelInfo = {\n\t\t\t\ttype = \"CLIPMODEL_AUTO\";\n\t\t\t\tsize = {\n\t\t\t\t\tx = 0;\n\t\t\t\t\ty = 0;\n\t\t\t\t\tz = 0;\n\t\t\t\t}\n\t\t\t\toffset = {\n\t\t\t\t\tx = 0;\n\t\t\t\t}\n\t\t\t\tnumSides = 0;\n\t\t\t\tclipModelName = " + moveableModel + ";\n\t\t\t}\n\t\t\tdormancy = {\n\t\t\t\tallowDormancy = true;\n\t\t\t}\n\t\t\tnetRelevancyFlags = \"\";\n")
            # elif "\"model\"" in mapcontent[(linecount + count)]:
            #     # parse model path
            #     modelPath = (current_line.split())[1]
            #     #modelPath = '"art/breakable/barrel/uac_tech_red_breakable.lwo"'
            #     #print(modelPath)
            #     idtech7map.write("\t\t\trenderModelInfo = {\n\t\t\t\tmodel = " + modelPath + ";\n\t\t\t\tscale = {\n\t\t\t\t\tx = " + str(scaleFactor) + ";\n\t\t\t\t\ty = " + str(scaleFactor) + ";\n\t\t\t\t\tz = " + str(scaleFactor) + ";\n\t\t\t\t}\t\t\t}\n")
            
            # static properties lines counter
            count = count + 1
            
            moveableCount = moveableCount + 1
            
        # close light structure with }
        idtech7map.write("\t\t}\n\t}\n}\n")
        
    
    # increment line counter
    linecount = linecount + 1
    
    

#------------------------------------------------
# parse idTech 4 particle emitters
#------------------------------------------------

# set line counter to 0 again
linecount = 0

# static also need ids
emitterCount = 1

for line in mapcontent:
    
    # static entity parse and write
    if "\"classname\" \"func_emitter" in line:
        
        # write static entity header
        idtech7map.write("entity {\n\tgroups {\n\t\t\"func_emitter\"\n\t}\n\tentityDef func_emitter_" + str(emitterCount) + " {\n\t\tinherit = \"func/emitter\";\n\t\tedit = {\n")
        
        # set counter to 1
        count = 1
        
        # until we have moveable properies
        while ("}" not in mapcontent[(linecount + count)]):
            
            # current line
            current_line = mapcontent[(linecount + count)]
            
            # search for known idTech 4 properties
            if "origin" in current_line:
                # parse coordinates
                originX = float(((current_line.split())[1])[1:]) * scaleFactor
                originY = float((current_line.split())[2]) * scaleFactor
                originZ = float(((current_line.split())[3])[:-1]) * scaleFactor
                #print(originX, originY, originZ)
                idtech7map.write("\t\t\tspawnPosition = {\n\t\t\t\tx = " + str(originX) + ";\n\t\t\t\ty = " + str(originY) + ";\n\t\t\t\tz = " + str(originZ) + ";\n\t\t\t}\n")
            elif "\"model\"" in mapcontent[(linecount + count)]:
                #emitter replace asset
                if "mc1_topvent.prt" in line:
                    emitterModel = "\"map_e2m3_core/vent_rolling_mist_ground\""
                elif "mc1_understeam.prt" in line:
                    emitterModel = "\"dlc1/mcity/floor_steam\""
                elif "mc1_hangar_pipe.prt" in line:
                    emitterModel = "\"dlc1/uac_oil_rig/pipe_spray_small\""
                else:
                    emitterModel = "\"map_e2m3_core/vent_rolling_mist_ground\""
                
                idtech7map.write("\t\t\tparticleSystem = " + emitterModel + ";\n")
                
            elif "rotation" in current_line:
                # parse rotation coordinates
                mat0X = float(((current_line.split())[1])[1:]) #* scaleFactor
                mat0Y = float((current_line.split())[2]) #* scaleFactor
                mat0Z = float((current_line.split())[3]) #* scaleFactor
                mat1X = float((current_line.split())[4]) #* scaleFactor
                mat1Y = float((current_line.split())[5]) #* scaleFactor
                mat1Z = float((current_line.split())[6]) #* scaleFactor
                mat2X = float((current_line.split())[7]) #* scaleFactor
                mat2Y = float((current_line.split())[8]) #* scaleFactor
                mat2Z = float(((current_line.split())[9])[:-1]) #* scaleFactor
                #print(originX, originY, originZ)
                idtech7map.write("\t\t\tspawnOrientation = {\n\t\t\t\tmat = {\n\t\t\t\t\tmat[0] = {\n\t\t\t\t\t\tx = " + str(mat0X) + ";\n\t\t\t\t\t\ty = " + str(mat0Y) + ";\n\t\t\t\t\t\tz = " + str(mat0Z) + ";\n\t\t\t\t\t}\n\t\t\t\t\tmat[1] = {\n\t\t\t\t\t\tx = " + str(mat1X) + ";\n\t\t\t\t\t\ty = " + str(mat1Y) + ";\n\t\t\t\t\t\tz = " + str(mat1Z) + ";\n\t\t\t\t\t}\n\t\t\t\t\tmat[2] = {\n\t\t\t\t\t\tx = " + str(mat2X) + ";\n\t\t\t\t\t\ty = " + str(mat2Y) + ";\n\t\t\t\t\t\tz = " + str(mat2Z) + ";\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n")
            
            # static properties lines counter
            count = count + 1
            
            emitterCount = emitterCount + 1
            
        # close light structure with }
        idtech7map.write("\t\t}\n\t}\n}\n")
        
    
    # increment line counter
    linecount = linecount + 1
    
    
# Add player start entity
idtech7map.write("entity {\n\tentityDef player_start_1 {\n\t\tinherit = \"player/start\";\n\t\tedit = {\n\t\t\tspawnPosition = {\n\t\t\t\tx = 29.6953;\n\t\t\t\ty = -35.1796875;\n\t\t\t}\n\t\t\tspawnOrientation = {\n\t\t\t\tmat = {\n\t\t\t\t\tmat[0] = {\n\t\t\t\t\t\tx = -1;\n\t\t\t\t\t\ty = -8.74227979e-08;\n\t\t\t\t\t}\n\t\t\t\t\tmat[1] = {\n\t\t\t\t\t\tx = 8.74227979e-08;\n\t\t\t\t\t\ty = -1;\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}")


# Closing map files once our job is done
idtech4map.close()
idtech7map.close()