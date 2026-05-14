# Sombra3d

Sombra3d is a standalone browser-based 3D asset studio for importing, creating, styling, slicing, rendering, and exporting production-ready 3D assets.


## What is included

- Single-file app in `index.html`
- Launch screen and full studio workspace
- 3D model import for common web formats, including GLB/GLTF and OBJ
- SVG-to-3D extrusion tools
- Image-to-3D heightmap generation
- Built-in primitive shapes
- Scene hierarchy, transform controls, material controls, lighting controls, and render presets
- Mesh smoothing, decimation, slicing, and knife-style cutting tools
- Screenshot, image export, GLB/OBJ export, and demo recording support
- Responsive layouts for desktop, tablet, and mobile screens

## Run locally

Open `index.html` directly in a modern browser.

For the most reliable file loading and export behavior, serve the folder from a local web server:

```bash
npx serve .
```

Then open the local URL printed by the server.

## Browser support

Use a current version of Chrome, Edge, Firefox, or another browser with WebGL support. Demo recording requires the browser `MediaRecorder` and `canvas.captureStream` APIs, so recording/export options may vary by browser.

## Project structure

```text
.
+-- index.html
`-- README.md
```

## Notes

The app depends on browser APIs and external CDN assets loaded by `index.html`. An internet connection may be required for fonts, logos, libraries, or remote image assets to render correctly.
