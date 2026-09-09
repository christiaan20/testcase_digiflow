import pikepdf
from pikepdf import Pdf, Name

from app.services import comment_operations


def dump_pdf_structure(obj, indent: int = 0, max_depth: int = 8, _seen=None) -> None:
    """Recursively print a pikepdf object structure."""
    allowed_keys = {"/AP":"# Overarching container of prerendered stream",
                    "/BBox":"# relative dimensions of the bounding box of the comment [<x> <y> <w> <h>]",
                    "/Subtype": "# type of the annotation",
                    "/Rect":"# absolute dimensions of the bounding box of the comment [<x1> <y1> <x2> <y2>]",
                    "/DA": "# Font information of comment",
                    "/Contents": "# Content of the comment",
                    "/N":"# Raw prerendered stream instruction to draw the comment"}


    if _seen is None:
        _seen = set()

    pad = "  " * indent
    if indent > max_depth:
        print(f"{pad}...")
        return

    if isinstance(obj, pikepdf.Dictionary):
        key = obj.objgen if obj.is_indirect else None
        if key and key in _seen:
            print(f"{pad}<<already shown {key}>>")
            return
        if key:
            _seen.add(key)
        print(f"{pad}<<")
        for k, v in obj.items():
            if k in allowed_keys.keys():
                print(f"{pad}  {k}: {allowed_keys[k]}")
                dump_pdf_structure(v, indent + 2, max_depth, _seen)
        print(f"{pad}>>")
    elif isinstance(obj, pikepdf.Array):
        print(f"{pad}[")
        for v in obj:
            dump_pdf_structure(v, indent + 1, max_depth, _seen)
        print(f"{pad}]")
    elif isinstance(obj, pikepdf.Stream):
        print(f"{pad}stream {dict(obj.stream_dict.items()) if obj.stream_dict else ''}")
        dump_pdf_structure(obj.stream_dict, indent + 1, max_depth, _seen)
    else:
        print(f"{pad}{obj}")


def show_comment_data(pdf: Pdf,print_info=False):

    for annot_index,annot in comment_operations.annot_iterator(pdf):

        content,ap_stream,raw_stream_str = comment_operations.extract_stream_data(annot)

        print(f"--------------- annotation {annot_index}----------------")
        print("# properties of the comment")
        dump_pdf_structure(annot)

        print("====================================")
        print("# Prerendered stream instructions to draw the comment")
        print_stream(raw_stream_str,print_info=print_info)
        print("====================================")



def print_stream(raw_stream_str ,print_info=False):

    if print_info:
        info = {" re W n": "# draw bounding box (<x> <y> <w> <h> re W n)",
                " rg": "# Set font color ( <r> <g> <b> rg)",
                " Td": "# move cursor to continue writing from (<x> <y> Td)",
                " Tf": "# set font (<font_name> <font_size> Tf",
                " Tj": "# Write text (<content> Tj)",
                }
        for line in raw_stream_str.split("\n"):
            comment = ""
            for k,v in info.items():
                if k in line:
                    comment = v
            print(f"{line}      {comment}")
    else:
        print(raw_stream_str)
