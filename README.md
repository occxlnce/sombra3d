# Sombra3D

Created with [Omma](https://omma.build)

## Setup

Install the Python dependencies and run the local application server:

```bash
python -m pip install -r requirements.txt
python server.py
```

Open `http://127.0.0.1:7000`. Serving the site through `server.py` is required for Hunyuan3D generation.

Set `HF_TOKEN` in your environment when the Hugging Face Space requires authentication or you need authenticated access. Never add the token to browser code.

## Image to 3D

Image and text generation uses the `tencent/Hunyuan3D-2` Hugging Face Space through the local `/api/image-to-3d` proxy. Choose **Create → Image → 3D** to upload an image, or **Create → Text → 3D** to start from a prompt. The generated GLB is imported directly into the current scene.

The Hunyuan integration supports:

- Image-to-3D, text-to-3D, or a prompt combined with an image.
- Textured generation through `/generation_all`.
- Geometry-only generation through `/shape_generation`.
- Automatic import of the returned GLB into the Studio scene.

Hugging Face Zero GPU availability and queue times can vary. For production use, point the same proxy contract at a dedicated Hunyuan3D deployment.

Local foreground extraction remains available through the Local Textured Relief, Solid Cutout, and Height Map modes.

For best results, upload images where the object is centered and clearly separated from the background.

## Workspace Projects

Use the Workspace button to save and reopen recent Sombra3D projects after refreshing or closing the browser. Projects are stored locally in IndexedDB, while the active project id is tracked in session storage.

The app also keeps an autosave project when there are scene changes, so the latest work can be recovered from the Workspace Projects modal.

## Camera Motion Templates

Use the Templates button near the camera controls to browse ready-made camera moves such as 360 Orbit, Hero Zoom In, Top Reveal, Side Sweep, Turntable Product Shot, Social Reel Motion, and Website Hero Loop.

Templates create a motion camera, add timeline keyframes, draw a camera path, and work with the existing Record Camera / Export MP4 workflow. You can preview a template, reset the preview, apply it to the timeline, and save current timeline camera paths as custom presets in local storage.

## Object Deconstruction

Imported model groups can be decomposed in the scene hierarchy:

- Select a child mesh row to edit, transform, hide, lock, duplicate, export, or delete that specific mesh.
- Use the `U` scene action, or press `U`, to ungroup a selected object into standalone mesh objects.
- Use Delete/Backspace on a selected mesh row to remove only that mesh from its parent object.
