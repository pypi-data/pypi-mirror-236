import math


def relu(inp):
  __name__ = "relu"
  if inp < 0:
    return 0
  else:
    return inp


def sigmoid(inp):
  __name__ = "sigmoid"
  return 1 / (1 + math.exp(-inp))


def straight(inp):
  __name__ = "straight"
  return inp


def binary(inp):
  __name__ = "binary"
  if inp < 0.5:
    return 0
  else:
    return 1


def leakyrelu(inp):
  __name__ = "leakyrelu"
  if inp < 0:
    return inp * 0.01
  else:
    return inp
