#!/bin/bash
# Cambia al modelo Qwen3.5-122B-A10B-FP8
cd "$(dirname "$0")"
echo "Parando modelo actual..."
docker compose --profile nvfp4 --profile fp8 --profile fp8-35b stop vllm-nvfp4 vllm-fp8 vllm-fp8-35b 2>/dev/null
docker compose --profile nvfp4 --profile fp8 --profile fp8-35b rm -f vllm-nvfp4 vllm-fp8 vllm-fp8-35b 2>/dev/null
echo "Arrancando FP8..."
docker compose --profile fp8 up -d
echo "Listo. Modelo FP8 arrancando en puerto 8000."
echo "Monitorear con: docker compose --profile fp8 logs -f vllm-fp8"
