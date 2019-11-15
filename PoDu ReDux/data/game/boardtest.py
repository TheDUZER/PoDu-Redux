"""
TO DO:

-Add function to select and move unit by changing pertinent attributes on unit and board
-Refine knockback function and checks for straight lines (Mewtwo, Rhyperior, etc)
"""

class TestUnit:
    def __init__(self):
        self.mp = 2
        self.location = "E4"

class BoardNeighbors:
    """Create generic board spaces and assign list of neighbor spaces"""
    def __init__(self, neighbors):
        self.neighbors = neighbors
        self.space_type = "board"
        self.force_stop = False
        self.force_attack = False
        self.occupied = False
        self.passable = True
        self.controlling_player = 0
        self.player_1_entry = False
        self.player_1_goal = False
        self.player_2_entry = False
        self.player_2_goal = False

class SpecialSpaces:
    def __init__(self, space_type):
        self.space_type = space_type
        if space_type != "Bench":
            self.occupied = False
        else:
            self.occupied = True

class ClassicBoardGenerator:
    """Create board object with space labels and adjusted bools for special spaces"""
    def __init__(self):
        #Populate neutral spaces of board
        self.A1 = BoardNeighbors({"B1":1, "B2":2, "A2":3})
        self.A1.player_1_entry = True
        self.A2 = BoardNeighbors({"A1":7, "A3":3})
        self.A3 = BoardNeighbors({"A2":7, "A4":3})
        self.A4 = BoardNeighbors({"A3":7, "A5":3})
        self.A4.player_1_goal = True
        self.A5 = BoardNeighbors({"A4":7, "A6":3, "B4":1})
        self.A6 = BoardNeighbors({"A5":7, "A7":3})
        self.A7 = BoardNeighbors({"A6":7, "B6":8, "B7":1})
        self.A7.player_1_entry = True
        self.B1 = BoardNeighbors({"A1":5, "C1":1})
        self.B2 = BoardNeighbors({"A1":6, "B4":3, "C2":1})
        self.B4 = BoardNeighbors({"B2":7, "A5":5, "B6":3})
        self.B6 = BoardNeighbors({"B4":7, "A7":5, "C6":1})
        self.B7 = BoardNeighbors({"A7":5, "C7":1})
        self.C1 = BoardNeighbors({"B1":5, "D1":1})
        self.C2 = BoardNeighbors({"B2":5, "D2":1})
        self.C6 = BoardNeighbors({"B6":5, "D6":1})
        self.C7 = BoardNeighbors({"B7":5, "D7":1})
        self.D1 = BoardNeighbors({"E1":1, "C1":5})
        self.D2 = BoardNeighbors({"E1":8, "D4":3, "C2":5})
        self.D4 = BoardNeighbors({"D2":7, "E3":1, "D6":3})
        self.D6 = BoardNeighbors({"D4":7, "E7":2, "C6":5})
        self.D7 = BoardNeighbors({"C7":5, "E7":1})
        self.E1 = BoardNeighbors({"D1":5, "E2":3, "D2":4})
        self.E1.player_2_entry = True
        self.E2 = BoardNeighbors({"E1":7, "E3":3})
        self.E3 = BoardNeighbors({"E2":7, "E4":3, "D4":5})
        self.E4 = BoardNeighbors({"E3":7, "E5":3})
        self.E4.player_2_goal = True
        self.E5 = BoardNeighbors({"E4":7, "E6":3})
        self.E6 = BoardNeighbors({"E5":7, "E7":3})
        self.E7 = BoardNeighbors({"E6":7, "D6":6, "D7":5})
        self.E7.player_2_entry = True

        #Populate list of Bench spaces for each player
        self.player_1_Bench = []
        for x in range(6):
            self.player_1_Bench.append(SpecialSpaces("Board"))
        self.player_2_Bench = []
        for x in range(6):
            self.player_2_Bench.append(SpecialSpaces("Board"))
            
        #Populate list of Ultra Space spaces for each player
        self.player_1_Ultra_Space = []
        for x in range(6):
            self.player_1_Ultra_Space.append(SpecialSpaces("Ultra Space"))
        self.player_2_Ultra_Space = []
        for x in range(6):
            self.player_2_Ultra_Space.append(SpecialSpaces("Ultra Space"))
            
        #Populate list of Eliminated spaces for each player
        self.player_1_Eliminated = []
        for x in range(6):
            self.player_1_Eliminated.append(SpecialSpaces("Eliminated"))
        self.player_2_Eliminated = []
        for x in range(6):
            self.player_2_Eliminated.append(SpecialSpaces("Eliminated"))

        #Populate list of PC spaces for each player
        self.player_1_PC = []
        for x in range(2):
            self.player_1_PC.append(SpecialSpaces("PC"))
        self.player_2_PC = []
        for x in range(2):
            self.player_2_PC.append(SpecialSpaces("PC"))
        
def knockback_pathing():
    """Check pathing for directional knockback effects"""
    #PENDING IMPLEMENTATION, NEEDS WORK
    direction = board.B2.neighbors["C2"]
    valid_moves = []

    for x in board.C2.neighbors.keys():
        if board.C2.neighbors[x] == direction:
            valid_moves.append(x)
        else:
            continue
                    
    #output -> ['D2']

def surround_check(focal_unit):
    """Checks for surround conditions of a target space"""
    #Needs differentiation between friendly and enemy players
    surround_counter = 0
    for x in eval(f"board.{focal_unit}.neighbors.keys()"):
        if eval(f"board.{x}.occupied") == True:
            continue
        else:
            surround_counter += 1
    if surround_counter == 0:
        return True
    else:
        return False

def path_check(focal_unit):
    """Check all possible paths for various purposes, including movement and teleports"""
    #need to add limitations for obstructed paths
    #need to boil for loops down to a recursive function

    global path_counter
    
    for x in eval(f"board.{focal_unit.location}.neighbors.keys()"):
        if eval(f"board.{x}.passable") == True:
            valid_moves.append(x)
        else:
            continue
        if focal_unit.mp > 1:
            for y in eval(f"board.{x}.neighbors.keys()"):
                if eval(f"board.{y}.passable") == True:
                    valid_moves.append(y)
                else:
                    continue
                if test_unit.mp > 2:
                    for z in eval(f"board.{y}.neighbors.keys()"):
                        if eval(f"board.{z}.passable") == True:
                            valid_moves.append(z)
                        else:
                            continue
                        if test_unit.mp > 3:
                            for a in eval(f"board.{z}.neighbors.keys()"):
                                if eval(f"board.{a}.passable") == True:
                                    valid_moves.append(a)
                                else:
                                    continue
                                if test_unit.mp > 4:
                                    for b in eval(f"board.{a}.neighbors.keys()"):
                                        if eval(f"board.{b}.passable") == True:
                                            valid_moves.append(b)
                                        else:
                                            continue
                                        if test_unit.mp > 5:        
                                            for c in eval(f"board.{b}.neighbors.keys()"):
                                                if eval(f"board.{c}.passable") == True:
                                                    valid_moves.append(c)
                                                else:
                                                    continue
                                                if test_unit.mp >6:
                                                    for d in eval(f"board.{c}.neighbors.keys()"):
                                                        if eval(f"board.{d}.passable") == True:
                                                            valid_moves.append(d)
                                                        else:
                                                            continue
                                                        if test_unit.mp >7:
                                                            for e in eval(f"board.{d}.neighbors.keys()"):
                                                                if eval(f"board.{e}.passable") == True:
                                                                    valid_moves.append(e)
                                                                else:
                                                                    continue
                                                                if test_unit.mp >8:
                                                                    for f in eval(f"board.{e}.neighbors.keys()"):
                                                                        if eval(f"board.{f}.passable") == True:
                                                                            valid_moves.append(f)
                                                                        else:
                                                                            continue
    return valid_moves
    path_counter = 0
##############################################################################

