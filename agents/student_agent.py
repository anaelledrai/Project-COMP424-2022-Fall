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
        if not adv_x == 0 and not chess_board[adv_x - 1, adv_y, self.dir_map["d"]]:
            if self.reachable(my_x, my_y, adv_x - 1, adv_y, max_step, 0, chess_board):
                return (adv_x - 1, adv_y), self.dir_map["d"]
        elif not adv_x == len(chess_board) - 1 and not chess_board[adv_x + 1, adv_y, self.dir_map["u"]]:
            if self.reachable(my_x, my_y, adv_x + 1, adv_y, max_step, 0, chess_board):
                return (adv_x + 1, adv_y), self.dir_map["u"]
        elif not adv_y == 0 and not chess_board[adv_x, adv_y - 1, self.dir_map["r"]]:
            if self.reachable(my_x, my_y, adv_x, adv_y - 1, max_step, 0, chess_board):   
                return (adv_x, adv_y - 1), self.dir_map["r"]
        elif not adv_y == len(chess_board) - 1 and not chess_board[adv_x, adv_y + 1, self.dir_map["l"]]:
            if self.reachable(my_x, my_y, adv_x, adv_y + 1, max_step, 0, chess_board):
                return (adv_x, adv_y + 1), self.dir_map["l"]
    
        return self.find_closest(my_x, my_y, adv_x, adv_y, max_step, 0, chess_board)
        # TODO: HANDLE OTHER CASES

    def find_closest(self, my_x, my_y, obj_x, obj_y, max_step, curr_step, chessboard):
        if max_step == curr_step:
            if not chessboard[my_x, my_y, 0] and not chessboard[my_x, my_y, 1] and not chessboard[my_x, my_y, 2] and not chessboard[my_x, my_y, 3]:
                return False
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
                val = self.find_closest(x, y, obj_x, obj_y, max_step, curr_step + 1, chessboard)
                if val:
                    return val
            
            return False


    def reachable(self, my_x, my_y, obj_x, obj_y, max_step, curr_step, chessboard):
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
                if self.reachable(x, y, obj_x, obj_y, max_step, curr_step + 1, chessboard):
                    return True

            return False 
            
            
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
            while chess_board[r, c, dir] or my_pos == adv_pos:
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