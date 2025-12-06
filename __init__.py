# __init__.py
# ComfyUI Resolution & AR Calculator (enhanced)
#
# Features:
# 1) Aspect ratios split into Portrait / Landscape dropdowns
# 2) Preset + Custom numeric longest side
# 3) Optional rounding to multiples of 64 for SD-friendly sizes

def _parse_ratio(aspect_ratio_str: str):
    """
    Accepts:
      - "7:9"
      - "7:9 (Modern Portrait)"
    Returns:
      (7, 9)
    """
    token = aspect_ratio_str.strip().split(" ")[0]
    w_ratio, h_ratio = map(int, token.split(":"))
    return w_ratio, h_ratio


def _round_to_multiple(value: int, base: int):
    # Round to nearest multiple of `base`, minimum `base`
    return max(base, int(round(value / base)) * base)


class ResolutionAspectCalculator:
    @staticmethod
    def calculate(longest_side_px: int, aspect_ratio: str, orientation: str):
        w_ratio, h_ratio = _parse_ratio(aspect_ratio)

        # Enforce orientation if requested
        if orientation == "landscape" and w_ratio < h_ratio:
            w_ratio, h_ratio = h_ratio, w_ratio
        elif orientation == "portrait" and w_ratio > h_ratio:
            w_ratio, h_ratio = h_ratio, w_ratio

        max_ratio = max(w_ratio, h_ratio)
        scale = longest_side_px / max_ratio

        width = round(w_ratio * scale)
        height = round(h_ratio * scale)

        return width, height, w_ratio, h_ratio


class ResolutionNode:
    """
    ComfyUI node wrapper.

    - Choose Aspect Group (Portrait/Landscape)
    - Pick ratio from the matching list
    - Choose longest side using preset or custom
    - Optionally round dimensions to multiples of 64
    """

    @classmethod
    def INPUT_TYPES(cls):
        # Based on your screenshot list
        portrait_ratios = [
            "1:1 (Perfect Square)",
            "2:3 (Classic Portrait)",
            "3:4 (Golden Ratio)",
            "3:5 (Elegant Vertical)",
            "4:5 (Artistic Frame)",
            "5:7 (Balanced Portrait)",
            "5:8 (Tall Portrait)",
            "7:9 (Modern Portrait)",
            "9:16 (Slim Vertical)",
            "9:19 (Tall Slim)",
            "9:21 (Ultra Tall)",
            "9:32 (Skyline)",
        ]

        landscape_ratios = [
            "1:1 (Perfect Square)",
            "3:2 (Golden Landscape)",
            "4:3 (Classic Landscape)",
            "5:3 (Wide Horizon)",
            "5:4 (Balanced Frame)",
            "7:5 (Elegant Landscape)",
            "8:5 (Cinematic View)",
            "9:7 (Artful Horizon)",
            "16:9 (Panorama)",
            "19:9 (Cinematic Ultrawide)",
            "21:9 (Epic Ultrawide)",
            "32:9 (Extreme Ultrawide)",
        ]

        return {
            "required": {
                "orientation": (["auto", "landscape", "portrait"], {"default": "auto"}),

                # Clearer than "long_side"
                "size_mode": (["preset", "custom"], {
                    "default": "preset",
                    "tooltip": "Use preset longest side or enter a custom value."
                }),

                "preset_longest_side_px": (["1000", "2000"], {
                    "default": "2000",
                    "tooltip": "Preset longest-edge sizes in pixels."
                }),

                # Custom numeric entry (shown alongside presets)
                "custom_longest_side_px": ("INT", {
                    "default": 2000,
                    "min": 256,
                    "max": 8192,
                    "step": 64,
                    "tooltip": "Custom longest edge in pixels (used only if size_mode=custom)."
                }),

                "aspect_group": (["portrait", "landscape"], {
                    "default": "portrait",
                    "tooltip": "Select which aspect ratio list to use."
                }),

                "aspect_ratio_portrait": (portrait_ratios, {"default": "7:9 (Modern Portrait)"}),
                "aspect_ratio_landscape": (landscape_ratios, {"default": "16:9 (Panorama)"}),

                # Rounding toggle
                "round_to_64": (["off", "on"], {
                    "default": "on",
                    "tooltip": "Rounds width/height to nearest multiple of 64 for SD-friendly sizes."
                }),
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution")
    FUNCTION = "process"
    CATEGORY = "Resolution Tools"

    def process(
        self,
        orientation,
        size_mode,
        preset_longest_side_px,
        custom_longest_side_px,
        aspect_group,
        aspect_ratio_portrait,
        aspect_ratio_landscape,
        round_to_64,
    ):
        # Pick longest side
        if size_mode == "custom":
            longest_side_px = int(custom_longest_side_px)
        else:
            longest_side_px = int(preset_longest_side_px)

        # Pick aspect ratio string from chosen group
        aspect_ratio = aspect_ratio_portrait if aspect_group == "portrait" else aspect_ratio_landscape

        # Base calculation
        width, height, w_ratio, h_ratio = ResolutionAspectCalculator.calculate(
            longest_side_px=longest_side_px,
            aspect_ratio=aspect_ratio,
            orientation=orientation,
        )

        # Optional rounding
        if round_to_64 == "on":
            width = _round_to_multiple(width, 64)
            height = _round_to_multiple(height, 64)

        resolution_string = f"{width}x{height}px"

        return (width, height, resolution_string)


NODE_CLASS_MAPPINGS = {
    "ResolutionNode": ResolutionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResolutionNode": "Resolution & AR Calculator"
}
