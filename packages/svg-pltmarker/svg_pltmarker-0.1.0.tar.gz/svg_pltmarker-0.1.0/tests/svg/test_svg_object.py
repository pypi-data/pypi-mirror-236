from pathlib import Path

from svg_pltmarker import SVGObject


if __name__ == "__main__":
    root_dir = Path(__file__).parent.parent.parent
    obj1 = SVGObject(str(root_dir / "data" / "python_logo_inkscape.svg"))
    obj2 = SVGObject(str(root_dir / "data" / "school.svg"))

    print(obj1)
    print(obj2)
