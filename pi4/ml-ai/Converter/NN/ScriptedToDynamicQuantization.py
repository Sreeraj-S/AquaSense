import torch.quantization

# Load the scripted model
scripted_model = torch.jit.load("pimodel/NN_model_scripted.pt")

# Apply dynamic quantization
quantized_model = torch.quantization.quantize_dynamic(
    scripted_model, {torch.nn.Linear}, dtype=torch.qint8
)
torch.jit.save(quantized_model, "pimodel/NN_model_quantized.pt")
