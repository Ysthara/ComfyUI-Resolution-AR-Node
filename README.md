# ComfyUI Resolution & AR Calculator

A lightweight ComfyUI custom node that converts a **target longest-side resolution + aspect ratio** into exact **width/height** for image generation.

This node is designed for people who want consistent size control across portrait/landscape formats without doing manual math every time.

---

## What this node does

Given:

- a **target longest side** (preset or custom),
- an **aspect ratio** (portrait or landscape list),
- and an optional **orientation override**,

the node outputs:

- **width (INT)**
- **height (INT)**
- **resolution (STRING)** like: `1344x1728px`

Optionally, it can auto-round to SD-friendly sizes.

---

## Key Features

### 1. Portrait & Landscape Aspect Ratio Lists
Aspect ratios are split into two curated dropdowns that match your reference list:

**Portrait list**
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

**Landscape list**
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

You choose which list to use via **Aspect Group**.

---

### 2. Preset + Custom Longest-Side
Instead of the confusing `long_side` name, the node uses:

- **size_mode**
  - `preset`
  - `custom`

- **preset_longest_side_px**
  - e.g., 1000, 2000 (you can extend)

- **custom_longest_side_px**
  - integer field with sensible min/max/step

This provides clarity and flexibility.

---

### 3. Orientation Override
You can set:

- `auto`
- `landscape`
- `portrait`

This acts as a **ratio normalization step**.

Example:
- You pick a portrait ratio like `7:9`
- But set orientation to `landscape`
- The node will swap it to behave like `9:7` before calculating.

It gives you an easy, explicit way to force output direction.

---

### 4. Optional Auto Rounding to Multiples of 64
A toggle:

- **round_to_64**
  - `on` (default)
  - `off`

This rounds both width and height to the nearest multiple of 64.

---

## Why rounding to multiples of 64 helps Stable Diffusion

Stable Diffusion models process images through a **downsampling pipeline** into a smaller latent space.

Most SD architectures effectively expect dimensions that are cleanly divisible by internal scaling steps (commonly 8, and more comfortably 64).

Rounding to **multiples of 64** is a widely used best practice because:

- It guarantees divisibility by **8**
- It aligns with common training sizes (e.g., 512, 768, 1024, 1152, 1280…)
- It often improves:
  - compositional stability,
  - memory predictability,
  - avoidance of edge-case resizing/padding behaviors.

**This is not strictly mandatory**, but it’s an excellent default for consistent results.

---

## Outputs

The node returns:

1. **width (INT)**
2. **height (INT)**
3. **resolution (STRING)**

You can wire `width` and `height` directly into:

- `KSampler.width`
- `KSampler.height`

---

## How the calculation works

### Step-by-step logic

1. The node reads an aspect ratio string like:

   `7:9 (Modern Portrait)`

2. It extracts only the ratio:

   `7:9`

3. It applies orientation override if needed:
   - If forced to landscape and ratio is portrait, it swaps.
   - If forced to portrait and ratio is landscape, it swaps.

4. It scales ratio to match the **target longest side**.

   Let:
   - target longest side = `L`
   - ratio = `w:h`

   Scale factor:

