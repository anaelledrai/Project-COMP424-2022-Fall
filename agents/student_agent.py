# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
from math import sqrt
from random import choice, randint

@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }
        self.autoplay = True

    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """
        adv_x, adv_y = adv_pos
        my_x, my_y = my_pos

        # Perform a check to determine if the 2 agents are in the same row or column
        if not adv_x == 0 and not chess_board[adv_x - 1, adv_y, self.dir_map["d"]] and not self.block_check(adv_x - 1, adv_y, chess_board) and not self.win_check(chess_board, (adv_x - 1, adv_y), (adv_x, adv_y), self.dir_map["d"]):
            if self.reachable(my_x, my_y, adv_x - 1, adv_y, adv_pos, max_step, 0, chess_board):
                return (adv_x - 1, adv_y), self.dir_map["d"]
        elif not adv_x == len(chess_board) - 1 and not chess_board[adv_x + 1, adv_y, self.dir_map["u"]] and not self.block_check(adv_x + 1, adv_y, chess_board) and not self.win_check(chess_board, (adv_x + 1, adv_y), (adv_x, adv_y), self.dir_map["u"]):
            if self.reachable(my_x, my_y, adv_x + 1, adv_y, adv_pos, max_step, 0, chess_board):
                return (adv_x + 1, adv_y), self.dir_map["u"]
        elif not adv_y == 0 and not chess_board[adv_x, adv_y - 1, self.dir_map["r"]] and not self.block_check(adv_x, adv_y - 1, chess_board) and not self.win_check(chess_board, (adv_x, adv_y - 1), (adv_x, adv_y), self.dir_map["r"]):
            if self.reachable(my_x, my_y, adv_x, adv_y - 1, adv_pos, max_step, 0, chess_board):   
                return (adv_x, adv_y - 1), self.dir_map["r"]
        elif not adv_y == len(chess_board) - 1 and not chess_board[adv_x, adv_y + 1, self.dir_map["l"]] and not self.block_check(adv_x, adv_y + 1, chess_board) and not self.win_check(chess_board, (adv_x, adv_y + 1), (adv_x, adv_y), self.dir_map["l"]):
            if self.reachable(my_x, my_y, adv_x, adv_y + 1, adv_pos, max_step, 0, chess_board):
                return (adv_x, adv_y + 1), self.dir_map["l"]
    
        val = self.find_closest(my_x, my_y, adv_x, adv_y, max_step, 0, chess_board)
        if val:
            return val
        else:
            return self.random_step(chess_board, my_pos, adv_pos, max_step)

    def block_check(self, my_x, my_y, chess_board):
        count = 0
        for i in range(4):
            if chess_board[my_x, my_y, i]:
                count += 1
        return count >= 2

    def win_check(self, chess_board, my_pos, adv_pos, dir):
        potential_chess_board = chess_board[:]
        potential_chess_board[my_pos[0], my_pos[1], dir] = True
        end, agent, adv =  self.check_endgame(potential_chess_board, my_pos, adv_pos)
        return end and adv >= agent

    def find_closest(self, my_x, my_y, obj_x, obj_y, max_step, curr_step, chessboard):
        if max_step == curr_step:
            if chessboard[my_x, my_y, 0] and chessboard[my_x, my_y, 1] and chessboard[my_x, my_y, 2] and chessboard[my_x, my_y, 3]:
                return False
            else:
                count = 0
                for i in range(4):
                    if chessboard[my_x, my_y, i]:
                        count += 1
                if count >= 2:
                    return False 

                if obj_x <= my_x and not chessboard[my_x, my_y, 2]:
                    dir = self.dir_map["d"]
                elif obj_x > my_x and not chessboard[my_x, my_y, 0]:
                    dir = self.dir_map["u"]
                else: 
                    dir = randint(0, 3)
                    while chessboard[my_x, my_y, dir]:
                        dir = randint(0, 3)
                        
                return (my_x, my_y), dir
        else:
            distances = {}
            if my_x + 1 < len(chessboard) and not chessboard[my_x, my_y, self.dir_map["d"]]:
                distances[(my_x + 1, my_y)] = abs(my_x + 1 - obj_x) + abs(my_y - obj_y)
            if my_x - 1 >= 0 and not chessboard[my_x, my_y, self.dir_map["u"]]:
                distances[(my_x - 1, my_y)] = abs(my_x - 1 - obj_x) + abs(my_y - obj_y)
            if my_y + 1 < len(chessboard) and not chessboard[my_x, my_y, self.dir_map["r"]]:
                distances[(my_x, my_y + 1)] = abs(my_x - obj_x) + abs(my_y + 1 - obj_y)
            if my_y - 1 >= 0 and not chessboard[my_x, my_y, self.dir_map["l"]]:
                distances[(my_x, my_y - 1)] = abs(my_x - obj_x) + abs(my_y - 1 - obj_y)

            positions = sorted(distances.items(), key=lambda kv: kv[1])
            for pos in positions:
                x, y = pos[0]

                if pos[0] == (obj_x, obj_y): 
                    continue
                val = self.find_closest(x, y, obj_x, obj_y, max_step, curr_step + 1, chessboard)
                if val:
                    return val
            
            return False


    def reachable(self, my_x, my_y, obj_x, obj_y, adv_pos, max_step, curr_step, chessboard):
        if my_x == obj_x and my_y == obj_y:
            return True
        elif max_step == curr_step:
            return False
        else:
            distances = {}    
            if my_x + 1 < len(chessboard) and not chessboard[my_x, my_y, self.dir_map["d"]]:
                distances[(my_x + 1, my_y)] = abs(my_x + 1 - obj_x) + abs(my_y - obj_y)
            if my_x - 1 >= 0 and not chessboard[my_x, my_y, self.dir_map["u"]]:
                distances[(my_x - 1, my_y)] = abs(my_x - 1 - obj_x) + abs(my_y - obj_y)
            if my_y + 1 < len(chessboard) and not chessboard[my_x, my_y, self.dir_map["r"]]:
                distances[(my_x, my_y + 1)] = abs(my_x - obj_x) + abs(my_y + 1 - obj_y)
            if my_y - 1 >= 0 and not chessboard[my_x, my_y, self.dir_map["l"]]:
                distances[(my_x, my_y - 1)] = abs(my_x - obj_x) + abs(my_y - 1 - obj_y)

            positions = sorted(distances.items(), key=lambda kv: kv[1])
            
            for pos in positions:
                x, y = pos[0]
                if pos[0] == adv_pos: 
                    continue
                if self.reachable(x, y, obj_x, obj_y, adv_pos, max_step, curr_step + 1, chessboard):
                    return True

            return False 

    def check_endgame(self, chess_board, my_pos, adv_pos):
        """
        Check if the game ends and compute the current score of the agents.

        Returns
        -------
        is_endgame : bool
            Whether the game ends.
        player_1_score : int
            The score of player 1.
        player_2_score : int
            The score of player 2.
        """
        # Union-Find
        father = dict()
        for r in range(len(chess_board)):
            for c in range(len(chess_board)):
                father[(r, c)] = (r, c)

        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]

        def union(pos1, pos2):
            father[pos1] = pos2

        for r in range(len(chess_board)):
            for c in range(len(chess_board)):
                for dir, move in enumerate(
                    ((0, 1), (1, 0))
                ):  # Only check down and right
                    if chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)

        for r in range(len(chess_board)):
            for c in range(len(chess_board)):
                find((r, c))
        p0_r = find(my_pos)
        p1_r = find(adv_pos)
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        if p0_r == p1_r:
            return False, p0_score, p1_score

        return True, p0_score, p1_score


    
            
    def random_step(self, chess_board, my_pos, adv_pos, max_step):
        ori_pos = my_pos[:]
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        steps = randint(0, max_step + 1)

        # Random Walk
        for _ in range(steps):
            r, c = my_pos
            dir = randint(0, 3)
            m_r, m_c = moves[dir]
            my_pos = (r + m_r, c + m_c)

            # Special Case enclosed by Adversary
            k = 0
            while chess_board[r, c, dir] or my_pos == adv_pos or self.win_check(chess_board, my_pos, adv_pos, dir):
                k += 1
                if k > 300:
                    break
                dir = randint(0, 3)
                m_r, m_c = moves[dir]
                my_pos = (r + m_r, c + m_c)

            if k > 300:
                my_pos = ori_pos
                break

        # Put Barrier
        dir = randint(0, 3)
        r, c = my_pos
        while chess_board[r, c, dir]:
            dir = randint(0, 3)

        return my_pos, dir