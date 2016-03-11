import copy
from policy import Policy
import numpy as np
from progressbar import ProgressBar


class MctsPolicy(Policy):
    def __init__(self, myid, board):
        super(MctsPolicy, self).__init__(myid, board)
        self._STATE = {}
        self._state_count = 0
        self._tree = []
        self._NS = {}
        self._N = {}
        self._Q = {}
        self._c = 0.5

    def put(self):
        self._tree = []
        self._NS = {}
        self._N = {}
        self._Q = {}
        iter = 3000
        perct = (iter / 100.)
        for i in range(3000):
            if i % perct == 0:
                print "simulation: %s %%" % (i / (perct))
            # if i%100 == 0:
            #    print "simulation:",i/100.
            self.simulate()
        s = self._board.to_state_string(self._myid)
        # print s
        a = self.select_move(s, self._board, self._myid)
        return a

    def simulate(self):
        board = copy.deepcopy(self._board)
        win_state = None
        cur = self._myid
        s_array, win_state, cur = self.sim_tree(board, cur)
        if win_state == None:
            win_state = self.sim_default(board, cur)
        self.backup(s_array, win_state)

    def sim_default(self, board, cur):
        while True:
            pos_x, pos_y = board.get_random_pos()
            board.put(cur, pos_x)
            if board.check_win(cur, pos_x, pos_y) == "WIN":
                if self._myid == cur:
                    win_state = 1
                    return win_state
                else:
                    win_state = -1
                    return win_state
            elif board.check_win(cur, pos_x, pos_y) == "EVEN":
                win_state = 0
                return win_state
            cur = self.get_next_player(cur)

    def sim_tree(self, board, cur):
        t = 0
        s_array = []
        while True:
            s = board.to_state_string(self._myid)
            a = None
            win_state = None
            # s_array.append(s)
            if s not in self._tree:
                self.new_node(s)
                # s_array.append([s, a])
                return s_array, win_state, cur
            else:
                pos_x = self.select_move(s, board, cur)
                pos_y = board.check_put(pos_x)
                s_array.append([s, pos_x])
                board.put(cur, pos_x)
                if board.check_win(cur, pos_x, pos_y) == "WIN":
                    if self._myid == cur:
                        win_state = 1
                        return s_array, win_state, cur
                    else:
                        win_state = -1
                        return s_array, win_state, cur
                elif board.check_win(cur, pos_x, pos_y) == "EVEN":
                    win_state = 0
                    return s_array, win_state, cur
                cur = self.get_next_player(cur)

    def select_move(self, s, board, cur):
        if self._myid == cur:
            a_array = self._Q[s] + self._c * np.sqrt(np.divide(self._NS[s], self._N[s]))
            a_array = sorted([x for x in enumerate(a_array)], key=lambda x: x[1], reverse=True)
            for ai in a_array:
                if board.check_put(ai[0]) != -1:
                    return ai[0]
            assert False
        else:
            a_array = self._Q[s] - self._c * np.sqrt(np.divide(self._NS[s], self._N[s]))
            a_array = sorted([x for x in enumerate(a_array)], key=lambda x: x[1], reverse=False)
            for ai in a_array:
                if board.check_put(ai[0]) != -1:
                    return ai[0]
            assert False

    def new_node(self, s):
        self._tree.append(s)
        self._NS[s] = 0.01
        self._N[s] = [0.01] * (self._board._bdata.shape[0])
        self._Q[s] = [0.01] * (self._board._bdata.shape[0])

    def backup(self, s_array, win_state):
        assert win_state != None
        # if win_state == None:
        #    return
        for sa in s_array:
            assert sa[1] != None
            # if sa[1] == None:
            #   return
            self._NS[sa[0]] += 1
            self._N[sa[0]][sa[1]] += 1
            self._Q[sa[0]][sa[1]] += (win_state - self._Q[sa[0]][sa[1]]) / self._N[sa[0]][sa[1]]

# return self.search_pick(self._myid, self._board)
