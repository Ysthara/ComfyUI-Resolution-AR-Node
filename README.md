# ComfyUI Resolution & AR Calculator

A simple ComfyUI utility node that calculates image width and height from a target longest-side value and an aspect ratio. It also provides an optional Stable Diffusion-friendly rounding mode.

This helps you pick consistent sizes for portrait, landscape, square, and ultrawide generations without doing manual math.

---

## Features

- Outputs:
  - Width (INT)
  - Height (INT)
  - Resolution label (STRING)

- Aspect ratios grouped into:
  - Portrait
  - Landscape

- Longest-side selection:
  - Presets (1K, 2K)
  - Custom numeric entry

- Orientation control:
  - Auto
  - Landscape
  - Portrait

- Optional rounding:
  - Round output dimensions to multiples of 64

---

## Installation

### Install with ComfyUI Manager

1. Open ComfyUI.
2. Open ComfyUI-Manager.
3. Choose the option to install a custom node from a URL.
4. Paste the repository URL.
5. Install.
6. Restart ComfyUI.

### Manual install

1. Open a terminal in your ComfyUI directory.
2. Run:

   git clone https://github.com/Ysthara/ComfyUI-Resolution-AR-Node

   inside:

   ComfyUI/custom_nodes/

3. Restart ComfyUI.

---

## Where to find the node

After restarting ComfyUI:

- Search for:
  Resolution & AR Calculator

- Or browse:
  Resolution Tools

---

## How to use

1. Add the node:
   Resolution & AR Calculator

2. Choose:
   - Orientation (Auto / Landscape / Portrait)
   - Size mode (Preset / Custom)
   - Longest side (Preset value or Custom value)
   - Aspect Group (Portrait / Landscape)
   - Aspect Ratio from the matching list
   - Rounding option (On / Off)

3. Connect:
   - width → KSampler.width
   - height → KSampler.height

---

## Aspect ratios included

### Portrait
- 1:1 (Perfect Square)
- 2:3 (Classic Portrait)
- 3:4 (Golden Ratio)
- 3:5 (Elegant Vertical)
- 4:5 (Artistic Frame)
- 5:7 (Balanced Portrait)
- 5:8 (Tall Portrait)
- 7:9 (Modern Portrait)
- 9:16 (Slim Vertical)
- 9:19 (Tall Slim)
- 9:21 (Ultra Tall)
- 9:32 (Skyline)

### Landscape
- 1:1 (Perfect Square)
- 3:2 (Golden Landscape)
- 4:3 (Classic Landscape)
- 5:3 (Wide Horizon)
- 5:4 (Balanced Frame)
- 7:5 (Elegant Landscape)
- 8:5 (Cinematic View)
- 9:7 (Artful Horizon)
- 16:9 (Panorama)
- 19:9 (Cinematic Ultrawide)
- 21:9 (Epic Ultrawide)
- 32:9 (Extreme Ultrawide)

---

## What “Round to 64” does

When enabled, the node rounds width and height to the nearest multiple of 64.

This is a common best practice for Stable Diffusion workflows because many model pipelines work most smoothly with dimensions that align with internal downsampling steps. In practice, this can improve reliability and reduce odd edge-case behavior in some setups.

If you need exact, unrounded dimensions, turn this option off.

---

## Example setups

### Modern portrait
- Aspect Group: Portrait
- Aspect Ratio: 7:9 (Modern Portrait)
- Size Mode: Preset
- Longest Side: 2K
- Round to 64: On

### Cinematic ultrawide
- Aspect Group: Landscape
- Aspect Ratio: 21:9 (Epic Ultrawide)
- Size Mode: Custom
- Longest Side: 2500
- Round to 64: On

### Exact sizing
- Round to 64: Off

---

## Troubleshooting

### The node does not appear
- Restart ComfyUI after installation.
- Confirm the repository folder is inside:
  ComfyUI/custom_nodes/

### Installation via Manager fails
- Try updating ComfyUI-Manager.
- Try manual installation.

---

## License

MIT
