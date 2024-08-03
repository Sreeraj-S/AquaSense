import torch

device = 'cpu'

# Load the TorchScript model
model = torch.jit.load("pimodel/NN_model_quantized.pt")  # or "model_quantized.pt"
model.eval()

# Example input tensor
test1 = torch.tensor([0, 1, 90/100, 90/100]).to(device)
print("Input tensor:", test1)

# Perform inference
with torch.no_grad():
    outputs = model(test1)

# Convert the output to the desired scale and print
result = int(outputs.item() * 5)
print("Output:", result)
