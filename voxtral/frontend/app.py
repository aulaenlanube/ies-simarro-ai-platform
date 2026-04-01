import os
import io
import base64
import httpx
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

VLLM_URL = os.environ.get("VLLM_URL", "http://localhost:8000")
MODEL = "mistralai/Voxtral-4B-TTS-2603"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/voices", methods=["GET"])
def get_voices():
    try:
        response = httpx.get(f"{VLLM_URL}/v1/audio/voices", timeout=10.0)
        response.raise_for_status()
        return jsonify(response.json())
    except httpx.ConnectError:
        return jsonify({"error": "TTS backend not available"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@app.route("/api/synthesize", methods=["POST"])
def synthesize():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    fmt = data.get("format", "wav")
    payload = {
        "input": text,
        "model": MODEL,
        "response_format": fmt,
        "voice": data.get("voice", "casual_male"),
    }

    speed = data.get("speed")
    if speed is not None:
        payload["speed"] = float(speed)

    instructions = data.get("instructions", "").strip()
    if instructions:
        payload["instructions"] = instructions

    ref_audio = data.get("ref_audio")
    if ref_audio:
        if not ref_audio.startswith(('http', 'data:', 'file://')):
            ref_audio = f"data:audio/wav;base64,{ref_audio}"
        payload["ref_audio"] = ref_audio
        payload["task_type"] = "CustomVoice"
        ref_text = data.get("ref_text", "").strip()
        if ref_text:
            payload["ref_text"] = ref_text

    mime_map = {
        "wav": "audio/wav",
        "mp3": "audio/mpeg",
        "flac": "audio/flac",
        "opus": "audio/ogg",
        "aac": "audio/aac",
        "pcm": "audio/pcm",
    }

    try:
        response = httpx.post(
            f"{VLLM_URL}/v1/audio/speech",
            json=payload,
            timeout=180.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        body = e.response.text[:500]
        return jsonify({"error": f"TTS error {e.response.status_code}: {body}"}), 502
    except httpx.ConnectError:
        return jsonify({"error": "TTS backend not available"}), 503

    return send_file(
        io.BytesIO(response.content),
        mimetype=mime_map.get(fmt, "audio/wav"),
        as_attachment=False,
        download_name=f"speech.{fmt}",
    )


@app.route("/api/voices/upload", methods=["POST"])
def upload_voice():
    if "audio_sample" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio_sample"]
    name = request.form.get("name", "").strip()
    ref_text = request.form.get("ref_text", "").strip()

    if not name:
        return jsonify({"error": "Voice name is required"}), 400

    files = {"audio_sample": (audio_file.filename, audio_file.read(), audio_file.content_type)}
    form_data = {"name": name, "consent": "true"}
    if ref_text:
        form_data["ref_text"] = ref_text

    try:
        response = httpx.post(
            f"{VLLM_URL}/v1/audio/voices",
            files=files,
            data=form_data,
            timeout=60.0,
        )
        response.raise_for_status()
        return jsonify(response.json())
    except httpx.HTTPStatusError as e:
        return jsonify({"error": f"Upload error {e.response.status_code}: {e.response.text[:300]}"}), 502
    except httpx.ConnectError:
        return jsonify({"error": "TTS backend not available"}), 503


@app.route("/api/voices/<name>", methods=["DELETE"])
def delete_voice(name):
    try:
        response = httpx.delete(f"{VLLM_URL}/v1/audio/voices/{name}", timeout=10.0)
        response.raise_for_status()
        return jsonify({"ok": True})
    except httpx.HTTPStatusError as e:
        return jsonify({"error": f"Delete error {e.response.status_code}"}), 502
    except httpx.ConnectError:
        return jsonify({"error": "TTS backend not available"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3100)
