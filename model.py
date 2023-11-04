import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = 'model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class DQNTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr  # step size
        self.gamma = gamma  # discount factor
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)  # used to update the model's parameters
        self.criterion = nn.MSELoss()  # used to measure the discrepancy between pred and target values

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        pred = self.model(state)
        target = pred.clone()

        Q_new = reward + self.gamma * torch.max(self.model(next_state)) * (1-done)  # Bellman equation
        target[torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()

        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()