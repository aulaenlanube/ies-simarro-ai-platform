# TITAN - Guía de configuración vLLM

## Hardware

- 3x NVIDIA RTX PRO 6000 Blackwell Max-Q (96 GB VRAM cada una = 288 GB total)
- Driver: 595.58 | CUDA: 13.2 | SO: Ubuntu 24.04

## Modelos disponibles

| Modelo | Cuantización | Contexto | GPUs | Puerto |
|---|---|---|---|---|
| Qwen/Qwen3.5-122B-A10B-FP8 | FP8 | 128K tokens | 0, 1 (tp=2) | 8000 |
| Sehyo/Qwen3.5-122B-A10B-NVFP4 | NVFP4 | 128K tokens | 0, 1 (tp=2) | 8000 |
| Qwen/Qwen3.5-35B-A3B-FP8 | FP8 | 128K tokens | 0, 1 (tp=2) | 8000 |

Los 3 modelos comparten las mismas GPUs y puerto, por lo que **solo uno puede estar activo a la vez**.

## Cambiar de modelo

Desde el directorio `~/PP1/compose/`:

```bash
# Cambiar al modelo 122B FP8
./switch-fp8.sh

# Cambiar al modelo 122B NVFP4
./switch-nvfp4.sh

# Cambiar al modelo 35B FP8
./switch-fp8-35b.sh
```

Los scripts se encargan de parar el modelo activo, eliminarlo y arrancar el nuevo. No hace falta hacer nada más — Open WebUI se reconecta automáticamente.

## Arranque manual

Si prefieres usar docker compose directamente:

```bash
# Arrancar 122B FP8
docker compose --profile fp8 up -d

# Arrancar 122B NVFP4
docker compose --profile nvfp4 up -d

# Arrancar 35B FP8
docker compose --profile fp8-35b up -d

# Parar todo
docker compose --profile fp8 --profile nvfp4 --profile fp8-35b down
```

## Monitorización

```bash
# Logs del modelo activo
docker logs -f titan-vllm

# Uso de GPUs
nvidia-smi

# Estado de los contenedores
docker ps
```

## Open WebUI

- URL: http://localhost:3000
- No requiere autenticación
- Se conecta automáticamente al modelo activo en el puerto 8000
