#!/bin/bash
# Arranca Voxtral TTS en GPU 2, puerto 8100
# Compatible con ComfyUI corriendo simultáneamente
cd "$(dirname "$0")"

echo "Arrancando Voxtral TTS en GPU 2..."
CUDA_VISIBLE_DEVICES=2 nohup ./venv/bin/vllm-omni serve mistralai/Voxtral-4B-TTS-2603 \
  --omni \
  --port 8100 \
  > voxtral.log 2>&1 &

echo "PID: $!"
echo "Monitorear con: tail -f ~/PP1/voxtral/voxtral.log"
