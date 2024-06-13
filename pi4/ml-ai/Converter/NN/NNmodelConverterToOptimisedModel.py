import torch
import torch.nn as nn


# Define the model architecture
class Model2NN(nn.Module):
    def __init__(self):
        super(Model2NN, self).__init__()
        self.layer = nn.Linear(4, 10)
        self.layer2 = nn.Linear(10, 10)
        self.layer3 = nn.Linear(10, 1)
        self.activation = nn.Sigmoid()

    def forward(self, X):
        X = torch.relu(self.layer(X))
        X = torch.relu(self.layer2(X))
        X = self.layer3(X)
        X = self.activation(X)
        return X


# Instantiate the model and load weights
device = torch.device('cpu')
model = Model2NN().to(device)
model.load_state_dict(torch.load("model/model2Data-1-10000-10pt_state.pt", map_location=device))
model.eval()

# Convert the model to TorchScript using tracing
example_input = torch.randn(1, 4).to(device)
scripted_model = torch.jit.trace(model, example_input)
torch.jit.save(scripted_model, "pimodel/NN_model_scripted.pt")
