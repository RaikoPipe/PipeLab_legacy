import numpy as np
from vpython import *
import interpret_path as pint
import weakref
import find_path as agt

# all dot objects are saved here
global topDotDict
topDotDict = weakref.WeakValueDictionary()
global wallDotDict
wallDotDict = weakref.WeakValueDictionary()

up = vector(0,1,0)
right =vector(1,0,0)
left = vector(-1,0,0)
down = vector(0,-1,0)

downtoleft = vector(1,0,0)
downtoright = vector(0,1,0)
lefttoup = vector(0,-1,0)
righttoup = vector(-1,0,0)
totop = vector(0,-0.9999,0)

upSG=vector(0, 4.5, 0)
rightSG=vector(4.5, 0, 0)
leftSG=vector(-4.5, 0, 0)
downSG=vector(0, -4.5, 0)

# downtoleft = vector(0,1,0)
# righttoup = vector(0,-1,0)
# lefttoup = vector(1,0,0)
# downtoright = vector(-1,0,0)
# totop = vector(0,0,-1)





# trasform numpy array into Vpython vector
def transformToVvector(npVector):
    x_coord = npVector[0]
    y_coord = npVector[1]
    z_coord = 15
    Vvector = vector(x_coord, y_coord, z_coord)
    return Vvector
    pass



def cdCm_Call(x_dots, y_dots, x_gap, y_gap ,dot_dist, wall_thickness, dot_color,wall_to_top_shift_dots, wall_visible, top_visible):
    global cMatrix
    cMatrix = create_dotCoord_Matrix(x_dots, y_dots, x_gap, y_gap, dot_dist, wall_thickness, dot_color,wall_to_top_shift_dots, wall_visible, top_visible)

def glG_Call(x_dots, y_dots):
    global boolGrid
    boolGrid = getlogicalGrid(x_dots, y_dots, cMatrix)
    return boolGrid


#adds object to reference dict
def remember(obj, dict):
    oid = id(obj)
    dict[oid] = obj
    return oid

#returns a positional vector depending on the object and its axis, that is used to place it correctly on the wall
def determineDirectionalOverhang(type, pipe_axis, overhang, width):

    if type == "corner":
        if pipe_axis == downtoleft: #from down to left
            direction = vector(-2.9, -2.9,5)
        elif pipe_axis == downtoright: # from down to right
            direction = vector(2.9,-2.9,5)
        elif pipe_axis == lefttoup: # from left to up
            direction = vector(-2.9, 2.9,5)
        elif pipe_axis == righttoup:
            direction = vector(2.9,2.9,5)# from right to up
        # elif pipe_axis == fromwall:
        #     direction = vector(0, 0.5, 7.85)
        elif pipe_axis == totop:
            direction = vector(0, 0.5, 7.85)
        else:
            print("pipe axis not recognized")
    else:
        if pipe_axis == up:  # to up
            direction = vector(0, -overhang, width)
        elif pipe_axis == right:  # to right
            direction = vector(-overhang, 0, width)
        elif pipe_axis == left:  # tp left
            direction = vector(overhang, 0, width)
        elif pipe_axis == down:
            direction = vector(0, overhang, width)  # is down
        else:
            print("direction of pipe not recognized")
    return direction

# creates a numpy array that acts as MBASE (contains 3D-build positions)
def create_dotCoord_Matrix(x_dots, y_dots, x_gap, y_gap ,dot_dist, wall_thickness, dot_color,wall_to_top_shift_dots, wall_visible, top_visible):

    coordinates_matrix = np.zeros((x_dots+1, y_dots+1), dtype="f,f,b")
    x_point = 1
    # create dots on wall
    add_x = x_gap  # variable for increasing x coordinate; 2.5cm is distance from end of wall
    # create dot along x axis
    for i in range(1, x_dots+1):
        add_y = y_gap  # variable for increasing y coordinate; 5cm is distance from top of wall
        y_point = 1
        #wallDot = sphere(pos=vector(add_x, add_y, wall_thickness), radius=1.3, color=dot_color, shininess=0,
        #      opacity=1, visible=wall_visible)
        #remember(wallDot, wallDotDict)
        coordinates_matrix[x_point, y_point] = (add_x, add_y, 0)

        # create dots along y axis
        for j in range(1, y_dots):
            y_point += 1
            add_y += dot_dist  # 10.5cm is y-distance between all dots
            #if j < wall_to_top_shift_dots:
            #    wallDot = sphere(pos=vector(add_x, add_y, wall_thickness), radius=1.3, color=dot_color, shininess=0,
            #           opacity=1, visible=wall_visible)
            #    remember(wallDot, wallDotDict)
            #else:
            #    topDot = sphere(pos=vector(add_x, add_y, wall_thickness), radius=1.3, color=dot_color, shininess=0,
            #           opacity=1, visible=top_visible)
            #    remember(topDot, topDotDict)

            coordinates_matrix[x_point, y_point] = (add_x, add_y, 0)

        pass
        add_x += dot_dist  # 10.5cm is x-distance between all dots
        x_point += 1
    pass
    "How do I create a compound with wall/top and spheres?"
    return coordinates_matrix
pass

#this has no use anymore
def setOccP_Call(pipe_pos, dotlength, pipe_ax):
    #setOccupancyPipe(pipe_pos, dotlength, pipe_ax, cMatrix)
    return

#this also has no use anymore
def setOccupancyPipe(pipe_pos, dotlength, pipe_ax, dcm):
    if pipe_ax == up:
        for i in range(dotlength):
            add_pos=(0,i)
            dcmChangePos = tuple(map(lambda c,k: c+k, add_pos, pipe_pos))
            dcm[dcmChangePos][2] = 1
    elif pipe_ax == left:
        for i in range(dotlength):
            add_pos=(-i,0)
            x_coord= pipe_pos
            dcmChangePos = tuple(map(lambda c,k: c+k, add_pos, pipe_pos))
            dcm[dcmChangePos][2] = 1
    elif pipe_ax == right:
        for i in range(dotlength):
            add_pos=(i,0)
            dcmChangePos = tuple(map(lambda c,k: c+k, add_pos, pipe_pos))
            dcm[dcmChangePos][2] = 1
    elif pipe_ax == down:
        for i in range(dotlength):
            add_pos=(0,-i)
            dcmChangePos = tuple(map(lambda c,k: c+k, add_pos, pipe_pos))
            dcm[dcmChangePos][2] = 1
    else:
            dcm[pipe_pos][2] = 1
    cMatrix = dcm


def setOccO_Call(pipe_pos, dotlength, pipe_ax):
    setOccupancyObstacle(pipe_pos, dotlength, pipe_ax, cMatrix)
    return

#sets obstacle positions on MBASE (cMatrix)
def setOccupancyObstacle(sizeX, sizeY, pos, dcm):
    j=0
    for i in range(sizeX):
        add_pos = (i, j)
        dcmChangePos = tuple(map(lambda c, k: c + k, add_pos, pos))
        dcm[dcmChangePos][2] = 1
        for j in range(sizeY):
            add_pos = (i, j)
            dcmChangePos = tuple(map(lambda c, k: c + k, add_pos, pos))
            dcm[dcmChangePos][2] = 1

    cMatrix = dcm

# returns a numpy array with all the occupied positions (M)
def getlogicalGrid(x_dots, y_dots, cMatrix):
    x = x_dots
    y = y_dots

    logicalGrid = np.tile(0, (x, y))
    y_point = 1
    # create dots on wall

    # get dots on y-axis
    for j in range(1, y_dots + 1):
        x_point = 1
        logicalGrid[x_point-1, y_point-1] = cMatrix[x_point, y_point][2]

        # get dots on x-axis
        for i in range(1, x_dots):
            x_point += 1
            logicalGrid[x_point-1, y_point-1] = cMatrix[x_point, y_point][2]

        pass
        y_point += 1
    pass
    return logicalGrid

def get_cMatrix():
    return cMatrix

def get_boolGrid():
    return boolGrid

#determines where pipe should be placed if two in a row are used
def determineSecondPipePlacement(pipe_axis, pipe_coord, secondPipeLength):
    if pipe_axis == up:
        vert = pipe_coord[1] + secondPipeLength
        hort = pipe_coord[0]
        secondPipeCoord = (hort,vert)
        return secondPipeCoord

    elif pipe_axis == left:
        vert = pipe_coord[1]
        hort = pipe_coord[0] - secondPipeLength
        secondPipeCoord = (hort,vert)
        return secondPipeCoord

    elif pipe_axis == right:
        vert = pipe_coord[1]
        hort = pipe_coord[0] + secondPipeLength
        secondPipeCoord = (hort,vert)
        return secondPipeCoord
    elif pipe_axis == down:
        vert = pipe_coord[1] - secondPipeLength
        hort = pipe_coord[0]
        secondPipeCoord = (hort,vert)
        return secondPipeCoord
    else:
        print("Unknown pipe_axis at coordinate: " + pipe_coord)

#determines where clamps should be put depending on obstacles and the most stable position
def determineClampPlacement(Matrix, a, n, type):
    if type == 3:
        print("here")
    axis = pint.getAxis(n)
    nLength = abs(n[0] - n[1])
    if nLength != type:
        nLength = nLength -1
    countList = []
    sorter = [int(type/2),3,1, 2, 4, 0, 5]
    for i in range(0,type):
        countList.append(i)
    aS = (a[0] - 1, a[1] - 1)
    left = (-axis[1], -axis[0])
    right = (axis[1], axis[0])
    # first best option: both sides are empty
    for i in sorter:  # check pos right of pipe
        if i not in countList:
            continue
        n_left = (left[0] + (axis[0] * (i)), left[1] + (axis[1] * (i)))
        b_left = (aS[0] + n_left[0], aS[1] + n_left[1])
        n_right = (right[0] + (axis[0] * (i)), right[1] + (axis[1] * (i)))
        b_right = (aS[0] + n_right[0], aS[1] + n_right[1])
        if not agt.outOfBounds(b_left, Matrix) and not agt.outOfBounds(b_right, Matrix):
            if Matrix[b_left] != 0 or Matrix[b_right] != 0:
                continue
            else:
                clampCoord = (aS[0] + i * axis[0] + 1, aS[1] + i * axis[1] + 1)
                return clampCoord
        else:
            clampCoord = (aS[0] + i * axis[0] + 1, aS[1] + i * axis[1] + 1)
            return clampCoord
    else:  # second best option: one side is empty
        for i in sorter:  # check pos right of pipe
            if i not in countList:
                continue
            n_left = (left[0] + (axis[0] * (i)), left[1] + (axis[1] * (i)))
            b_left = (aS[0] + n_left[0], aS[1] + n_left[1])
            n_right = (right[0] + (axis[0] * (i)), right[1] + (axis[1] * (i)))
            b_right = (aS[0] + n_right[0], aS[1] + n_right[1])
            if not agt.outOfBounds(b_left, Matrix) and not agt.outOfBounds(b_right, Matrix):
                if Matrix[b_left] != 0 and Matrix[b_right] != 0:
                    continue
                else:
                    clampCoord = (aS[0] + i * axis[0] + 1, aS[1] + i * axis[1] + 1)
                    break
            else:
                clampCoord = (aS[0] + i * axis[0] + 1, aS[1] + i * axis[1] + 1)
                break
        else:
            clampCoord = a
        return clampCoord

#determines what axis the corner should have depending on direction of pipes
def determineCorner(previousAxis, axis):
    if previousAxis == up and axis == up:
        cAxis = totop
    elif previousAxis == down and axis == down:
        cAxis = totop
    elif previousAxis == right and axis == up:
        cAxis = lefttoup
    elif previousAxis == left and axis == up:
        cAxis = righttoup
    elif previousAxis == right and axis == down:
        cAxis = downtoleft
    elif previousAxis == left and axis == down:
        cAxis = downtoright
    elif previousAxis == down and axis == right:
        cAxis = righttoup
    elif previousAxis == down and axis == left:
        cAxis = lefttoup
    elif previousAxis == up and axis == right:
        cAxis = downtoright
    elif previousAxis == up and axis == left:
        cAxis = downtoleft

    else:
        cAxis = up
        print("Error: CornerType cant be determined")
    return cAxis

# def determineCorner(previousAxis, axis):
#     if previousAxis == up and axis == up:
#         cAxis = totop
#     elif previousAxis == down and axis == down:
#         cAxis = totop
#     elif previousAxis == right and axis == up:
#         cAxis = up
#     elif previousAxis == left and axis == up:
#         cAxis = up
#     elif previousAxis == right and axis == down:
#         cAxis = down
#     elif previousAxis == left and axis == down:
#         cAxis = down
#     elif previousAxis == down and axis == right:
#         cAxis = right
#     elif previousAxis == down and axis == left:
#         cAxis = left
#     elif previousAxis == up and axis == right:
#         cAxis = right
#     elif previousAxis == up and axis == left:
#         cAxis = left
#
#     else:
#         cAxis = up
#         print("Error: CornerType cant be determined")
#     return cAxis

