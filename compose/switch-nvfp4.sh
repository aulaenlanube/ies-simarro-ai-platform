#!/bin/bash
# Cambia al modelo Qwen3.5-122B-A10B-NVFP4
cd "$(dirname "$0")"
echo "Parando modelo actual..."
docker compose --profile nvfp4 --profile fp8 --profile fp8-35b stop vllm-nvfp4 vllm-fp8 vllm-fp8-35b 2>/dev/null
docker compose --profile nvfp4 --profile fp8 --profile fp8-35b rm -f vllm-nvfp4 vllm-fp8 vllm-fp8-35b 2>/dev/null
echo "Arrancando NVFP4..."
docker compose --profile nvfp4 up -d
echo "Listo. Modelo NVFP4 arrancando en puerto 8000."
echo "Monitorear con: docker compose --profile nvfp4 logs -f vllm-nvfp4"
