from policy import Policy
from copy import deepcopy
import random

class DeepQPolicy(Policy):
  def __init__(self, myid, board, check_put, check_win):
    super( DeepQPolicy, self ).__init__( myid, board, check_put, check_win )

