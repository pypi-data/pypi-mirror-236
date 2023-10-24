from mnn import network,layer,weight
from mnn.activations import relu,sigmoid,straight,binary,leakyrelu
import logging


def geta(a):
  logger = logging.getLogger("mnn.load")
  a = a.strip()
  match a:
    case "relu":
      return relu
    case "sigmoid":
      return sigmoid
    case "straight":
      return straight
    case "binary":
      return binary
    case "leakyrelu":
      return leakyrelu
  logger.warn("Unknown activation function: '%s' using straight as default " % a)
  return straight
      
    

class load:
  def __init__(self,file_name):
    self.file_name = file_name


  def load(self):
    data = ""
    net = network()
    with open(self.file_name,"r") as f:
      data = f.read()
    start = False
    startpos = 0
    endpos = 0
    datalist = []
    for row in data.split("\n"):
      if " " not in row:
        if not start:
          start = True
          startpos = data.split("\n").index(row)
        else:
          start = False
          endpos = data.split("\n").index(row)
          datalist.append("\n".join(data.split("\n")[startpos:endpos]))
          start = True
          startpos = data.split("\n").index(row)


    datalist = [d for d in datalist if "" != d]
    for d in datalist:
      temp = d.split("\n")
      r = temp[0].split(",")
      a = temp[1]
      temp = temp[2:]
      lay = layer(int(r[0]),int(r[1]),geta(a))
      temp = "\n".join(temp)
      temp = temp.replace(a,"")
      temp2 = temp.split("\n\n")
      for n,w in zip(lay.neurons,temp2):
        w = w.replace(" ","")
        t = w.split("\n")
        # print(t)
        t = [float(i) for i in t]
        t = [weight.weight(i) for i in t]
        n.weights = t
        
        
      
      net.add_layer(lay)
    return net