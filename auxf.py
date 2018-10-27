import copy
#######################################################################################################################
#   function:   checks if a given point is part of a surrounded or an open string,
#               adding it to the open strings list in the latter case
#   input:      board, size of board, point being evaluated and list of points known to be part of open strings
#   output:     returns 1 if point's string is surrounded (game at terminal state)
#               returns 0 if point's string is not surrounded (has empty neighbour(s))
#######################################################################################################################
def is_string_surrounded(s, point, points_in_open_strings = []):
    state = copy.deepcopy(s)
    board = state[2:]
    n = state[0]

    string = [point]
    unchecked_buddies = [point]
    checked_buddies = []
    open = 0

    while len(unchecked_buddies) != 0:
        unchecked_buddy = unchecked_buddies[0]
        del unchecked_buddies[0]
        checked_buddies.extend([unchecked_buddy])
        neighbours = check_neighbourhood(state, unchecked_buddy)

        if 2 in neighbours:
            open = 1

        buddies_rel_coord = [index for index, value in enumerate(neighbours) if value == 1] #??????

        for buddy_rel_coord in buddies_rel_coord:
            buddy_coord = rel2abs_pos(unchecked_buddy, buddy_rel_coord)
            if buddy_coord not in string:
                string.extend(buddy_coord)
            if buddy_coord not in unchecked_buddies and buddy_coord not in checked_buddies:
                unchecked_buddies.extend([buddy_coord])

    if open == 1:
        points_in_open_strings.extend(string)
        return 0
    else:
        return 1

#######################################################################################################################
#   function:   checks the types of the 4 neighbours of a given point, i.e., whether each of these 4 points is either:
#               a board limit (-2) or a foe (-1), a buddy (1) or empty (2)
#   input:      state and coordinates of point whose neighbours we wish to id
#   output:     list containing the types of the 4 neighbours
#######################################################################################################################
def check_neighbourhood(s, point):
    state = copy.deepcopy(s)
    board = state[2:]
    n = state[0]

    neighbours = [0, 0, 0, 0]  # neighbours = (up, right, down, left)
    i = point[0]
    j = point[1]

    if i == 0:  # top row
        neighbours[0] = -2
        neighbours[2] = type_neighbour(board[i][j], board[i + 1][j])
    elif i > 0 and i < (n - 1):  # middle row
        neighbours[2] = type_neighbour(board[i][j], board[i + 1][j])
        neighbours[0] = type_neighbour(board[i][j], board[i - 1][j])
    elif i == (n - 1):  # bottom row
        neighbours[2] = -2
        neighbours[0] = type_neighbour(board[i][j], board[i - 1][j])

    if j == 0:  # left column
        neighbours[3] = -2
        neighbours[1] = type_neighbour(board[i][j], board[i][j + 1])
    elif j > 0 and j < (n - 1):  # middle column
        neighbours[3] = type_neighbour(board[i][j], board[i][j - 1])
        neighbours[1] = type_neighbour(board[i][j], board[i][j + 1])
    elif j == (n - 1):  # right column
        neighbours[1] = -2
        neighbours[3] = type_neighbour(board[i][j], board[i][j - 1])

    return neighbours

#######################################################################################################################
#   function:   finds the type of a neighbour regarding the current point (doesn't deal with limits of the board)
#   input:      current point, neighbour being tested
#   output:     type of neighbour: opponent (-1), buddy (1), empty point (2)
#######################################################################################################################
def type_neighbour(point, neighbour):
    if point == neighbour:
        return 1
    elif neighbour == 0:
        return 2
    else:
        return -1

#######################################################################################################################
#   function:   computes a point's absolute position given a reference point and a relative position
#   input:      reference point's coordinates, new point's relative position to it
#   output:     new point's absolute coordinates
#######################################################################################################################
def rel2abs_pos(point, rel):
        i = point[0]
        j = point[1]

        if rel == 0:
            return (i - 1, j)
        elif rel == 1:
            return (i, j + 1)
        elif rel == 2:
            return (i + 1, j)
        elif rel == 3:
            return (i, j - 1)