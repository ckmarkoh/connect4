import numpy as np
import policy
import minimaxPolicy
import deepqPolicy

WIDTH = 7
HEIGHT = 6
CONNECT = 4

BOARD = np.zeros((WIDTH, HEIGHT))


def check_put(pos, board):
  if pos < 0 or pos >= board.shape[0]:
    return -1
  if board[pos, 0] != 0:
    return -1 
  depth = 1
  while True:
    if depth >= board.shape[1]:
      break
    if board[pos, depth] != 0:
      break
    depth += 1
  return depth-1 


def put(idx, pos, board):
  if pos < 0 or pos >= board.shape[0]:
    return -1
  if board[pos, 0] != 0:
    return -1 
  depth = 1
  while True:
    if depth >= board.shape[1]:
      break
    if board[pos, depth] != 0:
      break
    depth += 1
  board[pos, depth-1] = idx 
  return depth-1 

def print_board(board, player):
  s = ""
  for i in range(board.shape[0]):
    s += "%s "%(i)
  s += '\n'
  for row in range(board.shape[1]):
    for col in range(board.shape[0]):
      s0 = "_ "
      if board[col, row] != 0:
        s0 = "%s "%( player[board[col, row]]["symbol"] )
      s += s0
    s += '\n'
  print s

def check_win(idx, posx, posy, board):
  s_function = [
   lambda x, y, d:(x+d, y), 
   lambda x, y, d:(x, y+d), 
   lambda x, y, d:(x+d, y+d),
   lambda x, y, d:(x+d, y-d), 
  ]
  def search_seq(idx, posx, posy, sdir, sfunc, board):
    posx, posy = sfunc(posx, posy, sdir)
    if posx < 0  or posx >= board.shape[0] or posy < 0 or posy >= board.shape[1]:
      return 0
    if board[posx, posy] != idx:
      return 0 
    else:
      count = 1
      count += search_seq(idx, posx, posy, sdir, sfunc, board)
      return count
  for s_fun in s_function:
    if search_seq(idx, posx, posy, -1, s_fun, board) + search_seq(idx, posx, posy, 1, s_fun, board) >= CONNECT - 1:
      return "WIN" 
  has_zero = False 
  for x in range(board.shape[0]):
    for y in range(board.shape[1]):
      if board[x, y] == 0:
        has_zero = True
        break
  if has_zero == False:
    return "EVEN" 
  else:
    return "NONE" 

  


PLAYER = {
  1:{"symbol":"x", "policy":policy.InputPolicy(1, BOARD, check_put, check_win)}, 
  #-1:{"symbol":"o", "policy":policy.RandomPolicy(-1, BOARD, check_put, check_win)}, 
  -1:{"symbol":"o", "policy":deepqPolicy.DeepQPolicy(-1, BOARD, check_put, check_win, "model.json")}, 
  }

#dqPolicy = deepqPolicy.DeepQPolicy(1,BOARD,check_put,check_win)
#dqPolicy.train()


def train():
  PLAYER[-1]["policy"].train("model2.json")

def play():
  print_board(BOARD, PLAYER)
  while True:
    winner = 0 
    for idx in PLAYER.keys():
      print "player :%s"%(PLAYER[idx]["symbol"])
      while True:
        posx = PLAYER[idx]["policy"].put()
        posy = put(idx, posx, BOARD)
        if posy == -1:
          print "invalid position"
        else:
          print_board(BOARD, PLAYER)
          win_result = check_win(idx, posx, posy, BOARD)
          if win_result == "WIN":
            winner = idx
          elif win_result == "EVEN":
            winner = 2 
          break
      if winner != 0:
        if winner in PLAYER.keys():
          print "winner is :%s"%(PLAYER[winner]["symbol"])
        else:
          print "even"
        break
    if winner != 0:
      break

if __name__ == "__main__":
  play()
