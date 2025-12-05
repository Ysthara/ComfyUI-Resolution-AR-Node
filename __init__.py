# __init__.py
# ComfyUI Resolution & AR Calculator custom node (Option A style)

def _parse_ratio(aspect_ratio_str: str):
    """
    Accepts:
      - "7:9"
      - "7:9 (Modern Portrait)"
    Returns:
      (7, 9)
    """
    # Take the first token before a space, e.g. "7:9"
    token = aspect_ratio_str.strip().split(" ")[0]
    w_ratio, h_ratio = map(int, token.split(":"))
    return w_ratio, h_ratio


class ResolutionAspectCalculator:
    @staticmethod
    def calculate(longest_side_px, aspect_ratio, orientation):
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

        resolution_string = f"{width}x{height}px"
        return width, height, resolution_string


class ResolutionNode:
    """
    ComfyUI node wrapper.
    Calculates width/height from:
      - longest_side_px: sets the LONGEST edge of the final image in pixels
      - aspect_ratio: "W:H (Name)"
      - orientation: auto / landscape / portrait
    """

    @classmethod
    def INPUT_TYPES(cls):
        aspect_ratios = [
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

                # Clearer name than "long_side"
                # Tooltip may be ignored by some UI builds, but is safe to include.
                "longest_side_px": (
                    ["1000", "2000"],
                    {
                        "default": "2000",
                        "tooltip": "Sets the longest edge of the final image in pixels."
                    }
                ),

                "aspect_ratio": (aspect_ratios, {"default": "1:1 (Perfect Square)"}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution")
    FUNCTION = "process"
    CATEGORY = "Resolution Tools"

    def process(self, orientation, longest_side_px, aspect_ratio):
        longest_side_px = int(longest_side_px)

        width, height, label = ResolutionAspectCalculator.calculate(
            longest_side_px=longest_side_px,
            aspect_ratio=aspect_ratio,
            orientation=orientation,
        )

        return (width, height, label)


NODE_CLASS_MAPPINGS = {
    "ResolutionNode": ResolutionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResolutionNode": "Resolution & AR Calculator"
}
