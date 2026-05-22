# Sombra3D

## Setup

Open `index.html` in your browser, or:

```bash
npx serve .
```

## Image to 3D

Image import now uses local foreground extraction by default. The importer samples the image border as background, removes edge-connected background, biases selection toward the centered object, and builds a textured relief/cutout from the remaining foreground.

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
