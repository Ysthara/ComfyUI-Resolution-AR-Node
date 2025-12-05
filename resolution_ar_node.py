# resolution_ar_node.py
#
# ComfyUI custom node that calculates width/height from:
# - long_side (1K or 2K)
# - aspect ratio (W:H)
# - orientation (auto / landscape / portrait)
#
# Outputs:
# - width (INT)
# - height (INT)
# - resolution string (STRING, e.g. "1000x1500px")

class ResolutionAspectCalculator:
    @staticmethod
    def calculate(long_side, aspect_ratio, orientation):
        w_ratio, h_ratio = map(int, aspect_ratio.split(":"))

        # Enforce orientation if requested
        if orientation == "landscape" and w_ratio < h_ratio:
            w_ratio, h_ratio = h_ratio, w_ratio
        elif orientation == "portrait" and w_ratio > h_ratio:
            w_ratio, h_ratio = h_ratio, w_ratio

        max_ratio = max(w_ratio, h_ratio)
        scale = long_side / max_ratio

        width = round(w_ratio * scale)
        height = round(h_ratio * scale)

        resolution_string = f"{width}x{height}px"
        return width, height, resolution_string


class ResolutionNode:
    """
    ComfyUI node wrapper.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "long_side": (["1000", "2000"], {"default": "2000"}),
                "aspect_ratio": ([
                    "1:1",
                    "2:3", "3:2",
                    "4:5", "5:4",
                    "7:9", "9:7",
                    "9:16", "16:9",
                ], {"default": "1:1"}),
                "orientation": (["auto", "landscape", "portrait"], {"default": "auto"}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution")
    FUNCTION = "process"
    CATEGORY = "Resolution Tools"

    def process(self, long_side, aspect_ratio, orientation):
        long_side = int(long_side)

        width, height, label = ResolutionAspectCalculator.calculate(
            long_side=long_side,
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
