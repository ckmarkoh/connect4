import random

class Policy(object):
  def __init__(self, myid, board, check_put, check_win):
    self._board = board 
    self._check_put = check_put
    self._check_win = check_win
    self._myid = myid
  def get_next_player(self, cur):
    if cur == 1:
      return -1
    else:
      return 1

class InputPolicy(Policy):
  def __init__(self, myid, board, check_put, check_win):
    super( InputPolicy, self ).__init__( myid, board, check_put, check_win )
  def put(self):
    posx = input(">")
    return posx

class RandomPolicy(Policy):
  def __init__(self, myid, board, check_put, check_win):
    super( RandomPolicy, self ).__init__( myid, board, check_put, check_win )
  def put(self):
    while True: 
      pos = int(random.random()*self._board.shape[0])
      if(self._check_put(pos,self._board) != -1):
        return pos
        
