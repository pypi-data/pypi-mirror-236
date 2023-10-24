class dataset:
  def __init__(self):
    self.inps = []
    self.outs = []
    self.count = 0

  def add_data(self,inp,out):
    self.inps.append(inp)
    self.outs.append(out)


  def get_next(self):
    temp =  (self.inps[self.count],self.outs[self.count])
    self.count += 1
    return temp

  def reset(self):
    self.count = 0