from policy import Policy
from copy import deepcopy
import random

class MinimaxPolicy(Policy):
  def __init__(self, myid, board, check_put, check_win):
    super( MinimaxPolicy, self ).__init__( myid, board, check_put, check_win )
    self._STATE = {}
    self._state_count = 0

  def put(self):
    return self.search_pick(self._myid, self._board)

  def search_pick(self, myid, board):
    score_max = -2.
    to_pick = 0
    for bx in range(self._board.shape[0]):
      by = self._check_put(bx, board)
      if by != -1:
        score = self.search_state_rec(myid, myid, bx, by, deepcopy(board))
        nx = self.get_next_player(myid)
        #print "states:",self._state_count
        self._state_count = 0
        #print "nx=%s, bx=%s,  score=%s"%(nx,  bx,  score)
        if score > score_max:
          score_max = score
          to_pick = bx
      #if score == score_max and random.random() > 0.7:
      #  to_pick = posx
    #print "state counts: %s"%(state_count)
    return to_pick

  def to_state_string(self, me, board):
    s = "%d"%(me+1)
    for row in range(board.shape[1]):
      for col in range(board.shape[0]):
        s += "%d"%( board[col, row]+1 )
    return s 

  
  def search_state_rec(self, me, cur, posx, posy, board):
    self._state_count += 1
    board[posx, posy] = cur 
    state_str = self.to_state_string(me, board)
    if state_str in self._STATE:
      return self._STATE[state_str]
    else:
      if self._check_win(cur, posx, posy, board) == "WIN":
        if me == cur:
          self._STATE[state_str] = 1.
        else:
          self._STATE[state_str] = -1.
      elif self._check_win(cur, posx, posy, board) == "EVEN":
        self._STATE[state_str] = 0.
      else:
        score_max, score_min = -2., 2.
        nx = self.get_next_player(cur)
        for bx in range(self._board.shape[0]):
          by = self._check_put(bx, board)
          if by != -1:
            state_next = deepcopy(board)
            score = self.search_state_rec(me, nx, bx, by, deepcopy(board))
            #print "nx=%s, bx=%s,  score=%s"%(nx,  bx,  score)
            if me != cur and score > score_max:
              score_max = score
            elif me == cur and score < score_min:
              score_min = score
            #if score_max == 1 and score_min == -1:
            #  break
        if me != cur:
          self._STATE[state_str] = score_max
          #return score_max 
        else:
          self._STATE[state_str] = score_min
          #return score_min 
      return self._STATE[state_str]
