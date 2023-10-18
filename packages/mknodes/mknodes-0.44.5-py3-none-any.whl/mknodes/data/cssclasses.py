from __future__ import annotations

import dataclasses


SCRIPT = """
var image = document.getElementsByClassName({class_name});
new simpleParallax(image, {
    orientation: 'right',
    scale: 1.5,
    overflow: true,
    delay: .6,
    transition: 'cubic-bezier(0,0,0,1)',
    maxTransition: 60
});
"""


def format_js_map(dct: dict) -> str:
    """Return JS map str for given dictionary.

    Arguments:
        dct: Dictionary to dump
    """
    rows = []
    for k, v in dct.items():
        match v:
            case bool():
                rows.append(f"    {k}: {str(v).lower()},")
            case None:
                rows.append(f"    {k}: null,")
            case _:
                rows.append(f"    {k}: {v!r},")
    row_str = "\n" + "\n".join(rows) + "\n"
    return f"{{{row_str}}}"


@dataclasses.dataclass(frozen=True)
class ParallaxEffect:
    orientation: str = "up"
    scale: float = 1.2
    overflow: bool = False

    def get_resources(self):
        pass


if __name__ == "__main__":
    dct = {
        "orientation": "right",
        "scale": 1.5,
        "overflow": True,
        "delay": 0.6,
        "transition": "cubic-bezier(0,0,0,1)",
        "maxTransition": 60,
    }
    result = format_js_map(dct)
    print(result)
