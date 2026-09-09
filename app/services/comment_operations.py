import pikepdf
from pikepdf import Name


def extract_stream_data(annot):
    content = annot.get("/Contents", "")
    ap = annot.get("/AP", None)
    if ap is None:
        return content,None,None

    # a set of instructions used to draw the comment
    ap_stream = ap.get("/N", None)
    if ap_stream is None or not isinstance(ap_stream, pikepdf.Stream):
        return content,None,None

    stream_data = ap_stream.read_bytes()
    raw_stream_str = stream_data.decode("latin-1", errors="ignore")

    return content,ap_stream,raw_stream_str


def move_comment_top_border(annot,diff):

        content,ap_stream,raw_stream_str = extract_stream_data(annot)

        index_height = 3

        # replace bounding boxes in annotation
        BBox_h = float(ap_stream.stream_dict["/BBox"][index_height])
        ap_stream.stream_dict["/BBox"][index_height] = BBox_h + diff

        Rect_h = float(annot["/Rect"][index_height])
        annot["/Rect"][index_height] = Rect_h + diff

        # replace bounding box line in prerendered stream with new bounding box dimensions
        replacement_dict= {}
        for line in raw_stream_str.splitlines():
            if " re W n" in line:
                values = line.split(" ")

                stream_box_h = float(values[index_height])
                values[index_height] = str(stream_box_h + diff)

                newline =  " ".join(values)
                replacement_dict[line] = newline

        for original,replacement in replacement_dict.items():
            raw_stream_str = raw_stream_str.replace(original, replacement)

        # write new raw_stream_str to ap_stream
        ap_stream.write(raw_stream_str.encode("latin-1"))

        return annot

def move_comment_left_border(annot, diff):
    content, ap_stream, raw_stream_str = extract_stream_data(annot)

    index_x = 0

    # replace bounding boxes in annotation
    BBox_x = float(ap_stream.stream_dict["/BBox"][index_x])
    ap_stream.stream_dict["/BBox"][index_x] = BBox_x + diff

    Rect_x = float(annot["/Rect"][index_x])
    annot["/Rect"][index_x] = Rect_x + diff

    # replace bounding box line in prerendered stream with new bounding box dimensions
    replacement_dict = {}
    for line in raw_stream_str.splitlines():
        if " re W n" in line:
            values = line.split(" ")

            stream_box_x = float(values[index_x])
            values[index_x] = str(stream_box_x + diff)

            newline = " ".join(values)
            replacement_dict[line] = newline

    for original, replacement in replacement_dict.items():
        raw_stream_str = raw_stream_str.replace(original, replacement)

    # write new raw_stream_str to ap_stream
    ap_stream.write(raw_stream_str.encode("latin-1"))

    return annot


def move_comment_bottom_border(annot, diff):
    content, ap_stream, raw_stream_str = extract_stream_data(annot)

    index_y = 1
    index_h = 3  # if the y is lowered the height of the relative boundary needs to be increased and vise-versa

    # replace bounding boxes in annotation
    BBox_h = float(ap_stream.stream_dict["/BBox"][index_h])
    ap_stream.stream_dict["/BBox"][index_h] = BBox_h - diff

    Rect_y = float(annot["/Rect"][index_y])
    annot["/Rect"][index_y] = Rect_y + diff

    # replace bounding box line in prerendered stream with new bounding box dimensions
    replacement_dict = {}
    for line in raw_stream_str.splitlines():
        if " re W n" in line:
            values = line.split(" ")

            stream_box_h = float(values[index_h])
            values[index_h] = str(stream_box_h - diff)

            newline = " ".join(values)
            replacement_dict[line] = newline
        if " Td" in line:
            values = line.split(" ")

            move_cursor_y = float(values[index_y])
            values[index_y] = str(move_cursor_y - diff)

            newline = " ".join(values)
            replacement_dict[line] = newline

    for original, replacement in replacement_dict.items():
        raw_stream_str = raw_stream_str.replace(original, replacement)

    # write new raw_stream_str to ap_stream
    ap_stream.write(raw_stream_str.encode("latin-1"))

    return annot


def move_comment_right_border(annot, diff):
    content, ap_stream, raw_stream_str = extract_stream_data(annot)

    index_width = 2

    # replace bounding boxes in annotation
    BBox_w = float(ap_stream.stream_dict["/BBox"][index_width])
    ap_stream.stream_dict["/BBox"][index_width] = BBox_w + diff

    Rect_w = float(annot["/Rect"][index_width])
    annot["/Rect"][index_width] = Rect_w + diff

    # replace bounding box line in prerendered stream with new bounding box dimensions
    replacement_dict = {}
    for line in raw_stream_str.splitlines():
        if " re W n" in line:
            values = line.split(" ")

            stream_box_w = float(values[index_width])
            values[index_width] = str(stream_box_w + diff)

            newline = " ".join(values)
            replacement_dict[line] = newline

    for original, replacement in replacement_dict.items():
        raw_stream_str = raw_stream_str.replace(original, replacement)

    # write new raw_stream_str to ap_stream
    ap_stream.write(raw_stream_str.encode("latin-1"))

    return annot

def move_text_vertically(annot,diff):
    content, ap_stream, raw_stream_str = extract_stream_data(annot)

    index_y = 1

    # replace bounding box line in prerendered stream with new bounding box dimensions
    replacement_dict = {}
    for line in raw_stream_str.splitlines():
        if " Td" in line:
            values = line.split(" ")

            move_cursor_y = float(values[index_y])
            values[index_y] = str(move_cursor_y + diff)

            newline = " ".join(values)
            replacement_dict[line] = newline

    for original, replacement in replacement_dict.items():
        raw_stream_str = raw_stream_str.replace(original, replacement)

    # write new raw_stream_str to ap_stream
    ap_stream.write(raw_stream_str.encode("latin-1"))

    return annot

def move_text_horizontally(annot,diff):
    content, ap_stream, raw_stream_str = extract_stream_data(annot)

    index_x = 0

    # replace bounding box line in prerendered stream with new bounding box dimensions
    replacement_dict = {}
    for line in raw_stream_str.splitlines():
        if " Td" in line:
            values = line.split(" ")

            move_cursor_x = float(values[index_x])
            values[index_x] = str(move_cursor_x + diff)

            newline = " ".join(values)
            replacement_dict[line] = newline

    for original, replacement in replacement_dict.items():
        raw_stream_str = raw_stream_str.replace(original, replacement)

    # write new raw_stream_str to ap_stream
    ap_stream.write(raw_stream_str.encode("latin-1"))

    return annot

def annot_iterator(pdf):
    for page_index, page in enumerate(pdf.pages):
        annots = page.get("/Annots", None)

        if annots is None:
            continue

        for annot_index,annot in enumerate(annots):
            try:
                if annot.get("/Subtype", None) != Name("/FreeText"):
                    continue
            except Exception:
                continue

            yield annot_index,annot

