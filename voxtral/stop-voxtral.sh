#!/bin/bash
# Para Voxtral TTS y opcionalmente arranca ComfyUI
cd "$(dirname "$0")"
echo "Parando Voxtral TTS..."
pkill -f "vllm-omni serve mistralai/Voxtral-4B-TTS-2603" 2>/dev/null
sleep 3
echo "Voxtral parado."

if [ "$1" = "--comfyui" ]; then
  echo "Arrancando ComfyUI..."
  docker start titan-comfyui
fi
