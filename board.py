import numpy as np
import random
random.seed(5)
import policy
import minimaxPolicy
import deepqPolicy


# PLAYER = {
#    1:{"symbol":"x", "policy":policy.InputPolicy(1, BOARD, check_put, check_win)},
#    #-1:{"symbol":"o", "policy":policy.RandomPolicy(-1, BOARD, check_put, check_win)},
#    -1:{"symbol":"o", "policy":deepqPolicy.DeepQPolicy(-1, BOARD, check_put, check_win, "model.json")},
#    }

class Board(object):
    def __init__(self, player):
        self._width = 7
        self._height = 6
        self._connect = 4
        #self._width = 5
        #self._height = 2
        #self._connect = 3
        self._player = player
        self._bdata = np.zeros((self._width, self._height))


    def to_state_string_str(self, me):
        s = "%d" % (me + 1)
        for row in range(self._bdata.shape[1]):
            s += " "
            for col in range(self._bdata.shape[0]):
                s += "%d" % (self._bdata[col, row] + 1)
        return s

    def to_state_string(self, me):
        s = (me + 1)
        for row in range(self._bdata.shape[1]):
            for col in range(self._bdata.shape[0]):
                s *= 3
                s += (self._bdata[col, row] + 1)
        return s

    def get_random_pos(self):
        while True:
            pos_x = int(random.random()*self._bdata.shape[0])
            pos_y = self.check_put(pos_x)
            if pos_y != -1:
                return pos_x,pos_y

    def check_put(self, pos):
        if pos < 0 or pos >= self._bdata.shape[0]:
            return -1
        if self._bdata[pos, 0] != 0:
            return -1
        depth = 1
        while True:
            if depth >= self._bdata.shape[1]:
                break
            if self._bdata[pos, depth] != 0:
                break
            depth += 1
        return depth - 1

    def put(self, idx, pos):
        assert pos >= 0 and pos <= self._bdata.shape[0]
        assert self._bdata[pos, 0] == 0
        depth = 1
        while True:
            if depth >= self._bdata.shape[1]:
                break
            if self._bdata[pos, depth] != 0:
                break
            depth += 1
        self._bdata[pos, depth - 1] = idx
        return depth - 1

    def putxy(self, idx, posx, posy):
        assert posx >= 0 and posx <= self._bdata.shape[0]
        assert posy >= 0 and posy <= self._bdata.shape[1]
        assert self._bdata[posx, posy] == 0
        self._bdata[posx, posy] = idx

    def print_board(self):
        s = ""
        for i in range(self._bdata.shape[0]):
            s += "%s " % (i)
        s += '\n'
        for row in range(self._bdata.shape[1]):
            for col in range(self._bdata.shape[0]):
                s0 = "_ "
                if self._bdata[col, row] != 0:
                    s0 = "%s " % (self._player[self._bdata[col, row]]["symbol"])
                s += s0
            s += '\n'
        print s

    def check_win(self, idx, posx, posy):
        s_function = [
            lambda x, y, d: (x + d, y),
            lambda x, y, d: (x, y + d),
            lambda x, y, d: (x + d, y + d),
            lambda x, y, d: (x + d, y - d),
        ]

        def search_seq(idx, posx, posy, sdir, sfunc):
            posx, posy = sfunc(posx, posy, sdir)
            if posx < 0 or posx >= self._bdata.shape[0] or posy < 0 or posy >= self._bdata.shape[1]:
                return 0
            if self._bdata[posx, posy] != idx:
                return 0
            else:
                count = 1
                count += search_seq(idx, posx, posy, sdir, sfunc)
                return count

        for s_fun in s_function:
            if search_seq(idx, posx, posy, -1, s_fun) + search_seq(idx, posx, posy, 1, s_fun) >= self._connect - 1:
                return "WIN"
        has_zero = False
        for x in range(self._bdata.shape[0]):
            for y in range(self._bdata.shape[1]):
                if self._bdata[x, y] == 0:
                    has_zero = True
                    break
        if has_zero == False:
            return "EVEN"
        else:
            return "NONE"
