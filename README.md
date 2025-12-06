# ComfyUI Resolution & AR Calculator

A lightweight ComfyUI custom node that converts a target longest-side resolution + aspect ratio into exact width/height for image generation.

This node is built for creators who want consistent, repeatable size control across portrait/landscape formats without manual math.

---

## What this node does

Given:
- a target longest side (preset or custom),
- an aspect ratio (portrait or landscape list),
- an optional orientation override,
- and an optional SD-friendly rounding option,

the node outputs:
- width (INT)
- height (INT)
- resolution (STRING), e.g. 1344x1728px

You can wire width/height directly into KSampler.

---

## Key Features

### 1) Portrait & Landscape Aspect Ratio Lists

Aspect ratios are split into two curated dropdowns that match your reference list.

Portrait list:
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

Landscape list:
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

You choose which list to use via:
- aspect_group: portrait | landscape

Note: ComfyUI inputs aren’t fully dynamic by default, so both dropdowns may be visible even though only one is used based on aspect_group.

---

### 2) Preset + Custom Longest-Side

To avoid confusion from “long_side”, the node uses:

- size_mode:
  - preset
  - custom

- preset_longest_side_px:
  - e.g. 1000, 2000 (easy to extend)

- custom_longest_side_px:
  - integer field with sane min/max/step

This lets you use quick presets for common workflows or precision control for specific targets.

---

### 3) Orientation Override

Orientation provides an explicit way to force shape behavior:

- auto
- landscape
- portrait

This works by normalizing the chosen ratio before scaling.

Example:
- You pick 7:9 (a portrait ratio)
- Set orientation to landscape
- The node swaps it to behave like 9:7 before calculation

This is helpful when you want to reuse the same labeled ratio list but force a consistent direction across a batch.

---

### 4) Optional Auto Rounding to Multiples of 64

Toggle:
- round_to_64: on | off

When enabled, the node rounds both width and height to the nearest multiple of 64.

---

## Why rounding to multiples of 64 helps Stable Diffusion

Stable Diffusion models generate images through a latent-space pipeline that relies on internal downsampling (commonly by factors of 8).

In practice:
- widths/heights divisible by 8 are generally safest,
- multiples of 64 are an even more comfortable standard for:
  - training alignment,
  - VRAM predictability,
  - avoiding edge-case resizing/padding behaviors,
  - overall workflow reliability.

This is not strictly required, but it is a solid best-practice default.
If you need exact print math or externally-matched dimensions, turn rounding off.

---

## Outputs

The node returns:
1) width (INT)
2) height (INT)
3) resolution (STRING)

Recommended wiring:
- width  -> KSampler.width
- height -> KSampler.height

---

## How the calculation works

1) The node reads an aspect ratio label like:
   7:9 (Modern Portrait)

2) It extracts the numeric ratio:
   7:9

3) Orientation override (if set):
   - landscape forces W >= H
   - portrait forces H >= W

4) Scale to match the target longest side:
   Let:
   - L = target longest side
   - ratio = w:h

   scale = L / max(w, h)

   width  = round(w * scale)
   height = round(h * scale)

5) Optional rounding:
   width  = nearest multiple of 64
   height = nearest multiple of 64

6) Format string:
   "{width}x{height}px"

---

## Installation

### Install with ComfyUI Manager (recommended)

1) Open ComfyUI
2) Open ComfyUI-Manager
3) Use Install from URL / Install via Git
4) Paste your repo URL:
   https://github.com/YOUR_USERNAME/ComfyUI-Resolution-AR-Node.git
5) Install
6) Restart ComfyUI

---

### Manual install via git

From your ComfyUI directory:

1) cd custom_nodes
2) git clone https://github.com/YOUR_USERNAME/ComfyUI-Resolution-AR-Node.git
3) Restart ComfyUI

---

## Required file structure

Because this node uses the “Option A” pattern (all code in __init__.py):

ComfyUI/custom_nodes/ComfyUI-Resolution-AR-Node/
- __init__.py
- README.md

ComfyUI will import the folder as a module and expects NODE_CLASS_MAPPINGS
to be available at the top level (in __init__.py).

---

## Where to find the node

After restarting ComfyUI:

- Search for:
  Resolution & AR Calculator

- Or browse category:
  Resolution Tools

---

## Usage examples

### Modern portrait batch
- aspect_group: portrait
- aspect_ratio_portrait: 7:9 (Modern Portrait)
- size_mode: preset
- preset_longest_side_px: 2000
- round_to_64: on

### Cinematic ultrawide
- aspect_group: landscape
- aspect_ratio_landscape: 21:9 (Epic Ultrawide)
- size_mode: custom
- custom_longest_side_px: 2500
- round_to_64: on

### Exact math mode (no SD rounding)
- round_to_64: off

---

## Customization

### Add more preset sizes

Edit:
- preset_longest_side_px list

Example:
- 1000, 1500, 2000, 3000, 4000

---

### Add more aspect ratios

Add strings to:
- portrait_ratios
- landscape_ratios

Format:
- W:H (Label)

---

## Limitations

- The ComfyUI UI may show both portrait and landscape dropdowns even though only one is used based on aspect_group.
- Rounding can slightly shift the exact longest side target.

---

## Troubleshooting

### “Skip module due to lack of NODE_CLASS_MAPPINGS”
Make sure __init__.py contains:
- NODE_CLASS_MAPPINGS = {...}

---

### “__init__.py not found”
Ensure your custom node folder contains __init__.py.

---

### Node not appearing
- Restart ComfyUI
- Check console logs
- Confirm the folder is directly under:
  ComfyUI/custom_nodes/

---

## License

Recommended:
- MIT License

---

## Summary

This node provides:
- clean aspect ratio selection split by orientation,
- presets + custom longest-side control,
- optional SD-friendly rounding to multiples of 64,
- and direct width/height outputs for seamless KSampler wiring.

It’s designed to reduce friction and make resolution selection fast, consistent, and human-readable.
