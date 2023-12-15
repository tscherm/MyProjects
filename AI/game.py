import random
import heapq
import copy
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    global MAX_DEPTH
    MAX_DEPTH = 3

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        global start
        start = time.time()

        num = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    num += 1

        drop_phase = True if num < 4 else False  # DONE: detect drop phase

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            moveVal = self.max_value(state, 0)
            #print("TIME:", time.time() - start)
            #print(moveVal[0])
            return moveVal[1]
        elif num >= 1:
            # Dont have random drop during drop phase
            # could combine just to make it changable if thats wrong
            moveVal = self.max_value(state, 0)
            #print("TIME:", time.time() - start)
            #print(moveVal[0])
            return moveVal[1]
        else: # num == 0
            if state[2][2] == ' ':
                return [(2, 2)]
            else:
                return [(3, 2)]
        

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []
        (row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))

        return move

    #returns PQ of moves based on heuristic/game value for the state
    #iterate in reverse order for MinVal function to give best moves for Min player
    def succ(self, state, toMove):
        pointList = list()
        succsPQ = []

        #find all points
        for row in range(5):
            for col in range(5):
                if state[row][col] == toMove:
                    pointList.append((row, col))
        #print("OG:", state)
        #drop phase all open points
        if len(pointList) < 4:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        newState = copy.deepcopy(state)

                        newState[row][col] = toMove

                        if toMove == self.my_piece:
                            toAdd = (-1*self.heuristic_game_value(newState), newState, [(row, col)])
                        else:
                            toAdd = (self.heuristic_game_value(newState), newState, [(row, col)])
                        heapq.heappush(succsPQ, toAdd)
            return succsPQ
                        
        #not drop phase find adjacent, open points
        for point in pointList:
            for r in range(-1, 2):
                if point[0] + r < 0 or point[0] + r > 4:
                    continue
                for c in range(-1, 2):
                    if point[1] + c < 0 or point[1] + c > 4:
                        continue
                    if state[point[0] + r][point[1] + c] == ' ':
                        newState = copy.deepcopy(state)

                        newState[point[0]][point[1]] = ' '
                        newState[point[0] + r][point[1] + c] = toMove

                        if toMove == self.my_piece:
                            toAdd = (-1*self.heuristic_game_value(newState), newState, [(point[0] + r, point[1] + c), point])
                        else:
                            toAdd = (self.heuristic_game_value(newState), newState, [(point[0] + r, point[1] + c), point])
                        heapq.heappush(succsPQ, toAdd)

        return succsPQ

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(4):
            row = i // 2
            col = i % 2

            if state[row][col] == ' ':
                continue
            
            if state[row][col] == state[row + 1][col + 1]  == state[row + 2][col + 2] == state[row + 3][col + 3]:
                return 1 if state[row][col] == self.my_piece else -1
                
        # TODO: check / diagonal wins
        for i in range(4):
            row = i // 2
            col = 4 - (i % 2)

            if state[row][col] == ' ':
                continue
            
            if state[row][col] == state[row + 1][col - 1] == state[row + 2][col - 2] == state[row + 3][col - 3]:
                return 1 if state[row][col] == self.my_piece else -1
        
        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] == ' ':
                    continue
                if state[row][col] == state[row][col + 1] == state[row + 1][col] == state[row + 1][col + 1]:
                    return 1 if state[row][col] == self.my_piece else -1
                    

        return 0 # no winner yet

    def heuristic_game_value(self, state):

        #check if it is a win
        win = self.game_value(state)
        if win != 0:
            return win
        
        #Step Distance (favors neither stacks or diags)
        axPoints = list()
        inPoints = list()

        for row in range(5):
            for col in range(5):
                if state[row][col] == ' ':
                    continue
                if state[row][col] == self.my_piece:
                    axPoints.append((row, col))
                else:
                    inPoints.append((row, col))

        axDist = 0
        inDist = 0

        # distance of how many steps (if unobstructed by other things) to its other points

        # during drop phase

        # case when 2 points for b and one for r
        if len(axPoints) == 2 and len(inPoints) == 1:
            axDist = max(abs(axPoints[0][0] - axPoints[1][0]), abs(axPoints[0][1] - axPoints[1][1]))
            hVal = 1/axDist - .75
            return hVal
            
        
        # case when there are 0 or 1 points for either b or r
        
        if len(inPoints) <= 1 or len(axPoints) <= 1:
            return 0
        
        # case when heuristic starts to matter
        # when b and r have less than 4 or b has 4 and r has 3
        if len(inPoints) < 4 or len(axPoints) < 4:
            for i in range(len(axPoints) - 1):
                for j in range(i + 1, len(axPoints)):
                    axDist += max(abs(axPoints[i][0] - axPoints[j][0]), abs(axPoints[i][1] - axPoints[j][1]))
            for i in range(len(inPoints) - 1):
                for j in range(i + 1, len(inPoints)):
                    inDist += max(abs(inPoints[i][0] - inPoints[j][0]), abs(inPoints[i][1] - inPoints[j][1]))

            hVal = (len(axPoints)-1)/axDist - (len(inPoints)-1)/inDist
            #print("HVAL:", hVal)
            return hVal
        
        else:
            for i in range(3):
                for j in range(i + 1, 4):
                    axDist += max(abs(axPoints[i][0] - axPoints[j][0]), abs(axPoints[i][1] - axPoints[j][1]))
                    inDist += max(abs(inPoints[i][0] - inPoints[j][0]), abs(inPoints[i][1] - inPoints[j][1]))

        #with adjusting for three in a row or diag

        # check horizontal wins
        for row in state:
            for i in range(3):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2]:
                    if row[i] == self.my_piece:
                        axDist -= 1
                    else:
                        inDist -= 1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    if row[i] == self.my_piece:
                        axDist -= 1
                    else:
                        inDist -= 1

        # TODO: check \ diagonal wins
        for i in range(9):
            row = i // 3
            col = i % 3

            if state[row][col] == ' ':
                continue
            
            if state[row][col] == state[row + 1][col + 1] and state[row][col] == state[row + 2][col + 2]:
                if state[row][col] == self.my_piece:
                    axDist -= 1
                else:
                    inDist -= 1
                
        # TODO: check / diagonal wins
        for i in range(9):
            row = i // 3
            col = 4 - (i % 3)

            if state[row][col] == ' ':
               continue
            
            if state[row][col] == state[row + 1][col - 1] and state[row][col] == state[row + 2][col - 2]:
                if state[row][col] == self.my_piece:
                    axDist -= 1
                else:
                    inDist -= 1

        # avoid getting stuck in T -> Z -> t
        if axDist == 6:
            axDist = 7
        if inDist == 6:
            inDist = 7

        # 6 is the min distance of non-winning arrangement (T-shape) even though there are better
        # since bDist/rDist > 0 and non-infinite hVal max/min is +/-4/5 (max dist = 30)
        hVal = 6/axDist - 6/inDist
        #print("HVAL:", hVal)
        return hVal

    # calculate best path at depth from state
    def max_value(self, state, depth):
        # use PQ from succ pq to help runtime in finding
        # print("MAX VAL:", state)
        # (hval, state, (new spot, old spot))
        succs = self.succ(state, self.my_piece)

        maxScore = -1
        bestMove = succs[-1][2]

        linesInspected = 0

        #if depth == 0:
            #print(succs[0:3])
            #print(succs[len(succs)//2])
        # don't need to check for depth will do that on Min player
        for i in range(len(succs)):
            linesInspected += 1

            sta = heapq.heappop(succs)

            #check if there is a win (will be on first iteration)
            if i == 0 and -1*sta[0] == 1:
                return (-1*sta[0], sta[2])

            #if i == 0:
                #print(sta)

            #if depth == 0:
                #print(sta)
            
            # only inspect good lines
            if (-1*sta[0] < 0 and linesInspected > 2) or linesInspected > 5:
                #print("NO MORE GOOD MOVES")
                return (maxScore, bestMove)
            
            # to avoid running out of time
            if time.time() - start > 4.7:
                #print("CLOCK")
                #if depth == 0:
                    #print((maxScore, bestMove))
                    
                return (maxScore, bestMove)
           
            # update maxScore and best move
            oppNextValue = self.min_value(sta[1], depth)[0]

            if oppNextValue > maxScore:
                maxScore = oppNextValue
                bestMove = sta[2]

        return (maxScore, bestMove)
        
    def min_value(self, state, depth):

        #print("MIN VAL:", state)

        succs = self.succ(state, self.opp)

        # need to check for depth on Min player and if there is a win
        if depth == MAX_DEPTH or succs[-1][0] == -1:
            return (succs[-1][0], succs[-1][2])

        minScore = 1
        bestMove = succs[0][2]

        linesInspected = 0
        
        for i in range(len(succs)):
            linesInspected += 1

            sta = heapq.heappop(succs)

            # only inspect good lines
            if (sta[0] > 0 and linesInspected > 3) or linesInspected > 10:
                #print("NO MORE GOOD MOVES")
                return (minScore, bestMove)
            
            # to avoid running out of time
            if time.time() - start > 4.7:
                #print("CLOCK")
                return (minScore, bestMove)

            oppNextValue = self.max_value(sta[1], depth+1)[0]

            # update minScore (dont need best move, just for fun)
            if oppNextValue < minScore:
                minScore = oppNextValue
                bestMove = sta[2]

        # print("BEST MOVE", bestMove, minScore)
        return (minScore, bestMove)

        

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
