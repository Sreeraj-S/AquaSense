import torch.quantization

# Load the scripted model
scripted_model = torch.jit.load("pimodel/RNN_model_scripted.pt")

# Apply dynamic quantization
quantized_model = torch.quantization.quantize_dynamic(
    scripted_model, {torch.nn.Linear, torch.nn.RNN}, dtype=torch.qint8
)
torch.jit.save(quantized_model, "pimodel/RNN_model_quantized.pt")
