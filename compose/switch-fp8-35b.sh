#!/bin/bash
# Cambia al modelo Qwen3.5-35B-A3B-FP8
cd "$(dirname "$0")"
echo "Parando modelo actual..."
docker compose --profile nvfp4 --profile fp8 --profile fp8-35b stop vllm-nvfp4 vllm-fp8 vllm-fp8-35b 2>/dev/null
docker compose --profile nvfp4 --profile fp8 --profile fp8-35b rm -f vllm-nvfp4 vllm-fp8 vllm-fp8-35b 2>/dev/null
echo "Arrancando Qwen3.5-35B FP8..."
docker compose --profile fp8-35b up -d
echo "Listo. Modelo 35B FP8 arrancando en puerto 8000."
echo "Monitorear con: docker compose --profile fp8-35b logs -f vllm-fp8-35b"
