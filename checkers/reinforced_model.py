import torch
import torch.nn as nn
import os

cur_path = os.path.dirname(__file__)

class Reinforcement_Network(nn.Module):
	def __init__(self) -> None:
		super().__init__()

		self.hidden1 = nn.Linear(32, 16)
		self.hidden2 = nn.Linear(16, 8)
		self.hidden3 = nn.Linear(8, 4)

		self.output = nn.Linear(4, 1)

		self.ReLu = nn.ReLU()

		self.sigmoid = nn.Sigmoid()


	def forward(self, x):
		x = self.hidden1(x)
		x = self.ReLu(x)
		x = self.hidden2(x)
		x = self.ReLu(x)
		x = self.hidden3(x)
		x = self.ReLu(x)
		x = self.output(x)
		x = self.sigmoid(x)

		return x
	
class Model:
	def __init__(self) -> None:
		self.model = Reinforcement_Network()
		self.model.load_state_dict(torch.load(cur_path + '/Q-Learning Model/results/reinforced_model.pth'))
	

	def move(self):
		pass


reinforced_model = Model()