import torch
import torch.nn as nn


# Define the model architecture
class RNNModel(nn.Module):
    def __init__(self, input_size=2, hidden_size=50, output_size=1, num_layers=2):
        super(RNNModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return torch.sigmoid(out)


# Instantiate the model and load weights
device = torch.device('cpu')
model = RNNModel().to(device)
model.load_state_dict(torch.load("model/RNNmodelDummySet-4-Loss_%12-final_state.pt", map_location=device))
model.eval()

# Convert the model to TorchScript using tracing
sequence_length = 7  # As inferred from your last_sequence
example_input = torch.randn(1, sequence_length, 2).to(device)  # Correct input shape for RNN
scripted_model = torch.jit.trace(model, example_input)
torch.jit.save(scripted_model, "pimodel/RNN_model_scripted.pt")
