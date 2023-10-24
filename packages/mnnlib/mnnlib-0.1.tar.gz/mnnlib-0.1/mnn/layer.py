from mnn.neuron import neuron


class layer:

  def __init__(self, input_count, output_count, act_func):
    self.inp_count = input_count
    self.out_count = output_count
    self.neurons = []
    for _ in range(output_count):
      self.neurons.append(neuron(input_count, act_func))

  def __str__(self):
    t = f"neuron count: {len(self.neurons)}"
    return t

  def get_weights(self):
    weights = []
    for n in self.neurons:
      weights += n.get_weights()
    return weights

  def run(self, input):
    temp = []
    for n in self.neurons:
      temp.append(n.run(input))
    return temp
