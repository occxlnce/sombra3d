import os
import shutil
import tempfile
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from gradio_client import Client, handle_file


ROOT = Path(__file__).resolve().parent
GENERATED_DIR = ROOT / "generated"
GENERATED_DIR.mkdir(exist_ok=True)

env_file = ROOT / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.strip().partition("=")
        if separator and key and not key.startswith("#"):
            os.environ.setdefault(key, value)

app = Flask(__name__, static_folder=None)
client = None


def get_client():
    global client
    if client is None:
        client = Client("tencent/Hunyuan3D-2", hf_token=os.getenv("HF_TOKEN") or None, verbose=False)
    return client


def number(value, default, minimum, maximum):
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))


@app.post("/api/image-to-3d")
def image_to_3d():
    image = request.files.get("image")
    prompt = (request.form.get("prompt") or "").strip()
    if not image and not prompt:
        return jsonify(error="Upload an image or enter a text prompt."), 400

    textured = request.form.get("textured", "true").lower() != "false"
    api_name = "/generation_all" if textured else "/shape_generation"
    temporary_path = None

    try:
        image_input = None
        if image:
            suffix = Path(image.filename or "input.png").suffix or ".png"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temporary_file:
                image.save(temporary_file)
                temporary_path = temporary_file.name
            image_input = handle_file(temporary_path)

        generation_options = dict(
            caption=prompt or None,
            image=image_input,
            mv_image_front=None,
            mv_image_back=None,
            mv_image_left=None,
            mv_image_right=None,
            steps=int(number(request.form.get("steps"), 30, 1, 100)),
            guidance_scale=number(request.form.get("guidanceScale"), 5, 1, 20),
            seed=int(number(request.form.get("seed"), 1234, 0, 10_000_000)),
            octree_resolution=int(number(request.form.get("octreeResolution"), 256, 16, 512)),
            check_box_rembg=request.form.get("removeBackground", "true").lower() != "false",
            num_chunks=int(number(request.form.get("numChunks"), 8000, 1000, 5_000_000)),
            randomize_seed=request.form.get("randomizeSeed", "true").lower() != "false",
        )
        used_geometry_fallback = False
        try:
            result = get_client().predict(api_name=api_name, **generation_options)
        except Exception as generation_error:
            # The public Space occasionally raises only "NameError" from its
            # textured pipeline. Preserve generation by retrying its shape API.
            if textured and "NameError" in repr(generation_error):
                app.logger.warning("Hunyuan textured generation failed; retrying shape generation")
                result = get_client().predict(api_name="/shape_generation", **generation_options)
                used_geometry_fallback = True
            else:
                raise

        candidates = result if isinstance(result, (list, tuple)) else [result]
        source = None
        for candidate in reversed(candidates[:2] if textured else candidates[:1]):
            candidate_path = (candidate.get("path") or candidate.get("value")) if isinstance(candidate, dict) else candidate
            if isinstance(candidate_path, (str, os.PathLike)) and Path(candidate_path).is_file():
                source = Path(candidate_path)
                break
        if not source:
            raise RuntimeError("Hunyuan3D did not return a downloadable model file.")

        asset_id = uuid.uuid4().hex
        extension = source.suffix.lower() if source.suffix.lower() in {".glb", ".gltf", ".obj"} else ".glb"
        destination = GENERATED_DIR / f"{asset_id}{extension}"
        shutil.copy2(source, destination)

        return jsonify(
            status="completed",
            name=prompt or Path(image.filename or "Hunyuan3D Asset").stem,
            modelUrl=f"/api/generated/{destination.name}",
            warning="The textured service was unavailable, so a geometry-only model was generated." if used_geometry_fallback else None,
        )
    except Exception as error:
        app.logger.exception("Hunyuan3D generation failed")
        message = str(error).strip("'\"")
        if message == "NameError":
            message = "The upstream Hunyuan3D service failed internally. Please retry when its GPU service is available."
        return jsonify(error=message or type(error).__name__), 502
    finally:
        if temporary_path:
            Path(temporary_path).unlink(missing_ok=True)


@app.get("/api/generated/<path:filename>")
def generated_asset(filename):
    return send_from_directory(GENERATED_DIR, filename, as_attachment=False)


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/<path:filename>")
def static_file(filename):
    return send_from_directory(ROOT, filename)


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "7000")), debug=os.getenv("FLASK_DEBUG") == "1")
