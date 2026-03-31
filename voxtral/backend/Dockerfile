FROM vllm/vllm-omni:v0.18.0

# Reinstalar PyTorch con soporte Blackwell (cu128)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 --force-reinstall

ENTRYPOINT ["vllm"]
