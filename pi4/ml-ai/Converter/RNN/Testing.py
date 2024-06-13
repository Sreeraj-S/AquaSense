import numpy as np
import torch

device = 'cpu'

# Load the TorchScript model
scripted_model = torch.jit.load("pimodel/RNN_model_quantized.pt")
scripted_model.eval()

# Example input sequence
last_day = np.array([334, 335, 336, 337, 338, 339, 340]) / 365.0
last_day = np.round(last_day, 3)
avail = np.array([0,1, 0, 1, 0, 0, 0])
last_sequence = np.vstack((avail, last_day)).T
last_sequence_tensor = torch.tensor(last_sequence, dtype=torch.float32).unsqueeze(0).to(device)  # Shape: (1, sequence_length, 2)

# Perform inference
with torch.no_grad():
    next_day_avail = scripted_model(last_sequence_tensor).item()

print(last_sequence)
print(f'Predicted availability for the next day: {round(next_day_avail)}')
