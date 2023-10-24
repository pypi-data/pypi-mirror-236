import json

class network:
  def __init__(self):
    self.layers = []
    self.run_func = None

  def __str__(self):
    temp = ""
    for layer in self.layers:
      temp += f"  layer: {self.layers.index(layer)}, {layer.__str__()}\n"
    t = f"layer_count: {len(self.layers)}\n{temp}"
    return t

  def add_layer(self,layer):
    self.layers.append(layer)

  def run(self,input):
    if len(self.layers) == 0:
      raise Exception("No layers intilizsed")
      
    if len(input) != self.layers[0].inp_count:
      raise Exception(f"Input size {len(input)} does not match layer input size {self.layers[0].inp_count}")

    # temp = []
    # temp.append(input)
    

    for layer in self.layers:
      input = layer.run(input)
      # temp.append(input)
      
    # with open("temp.txt", "w") as f:
    #   json.dump(temp,f)
    
    return input

  def run_all_data(self,input):
    ins = input.inps
    r_outs = []
    for i in ins:
      r_outs.append(self.run(i))
    return r_outs,input.outs

  def get_weights(self):
    weights = []
    for layer in self.layers:
      weights += layer.get_weights()
    return weights