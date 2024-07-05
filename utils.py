import re


def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0: "", 1: "k", 2: "m", 3: "g", 4: "t"}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n] + "b"


def norm(value):
    """Normalize the color value from 0-65535 range to 0-255 range."""
    return int(value * 255 / 65535)


def rgb_to_hex(rgb):
    """Convert an RGB list to an HTML hex color string."""
    return "{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])


def recursive_4_space_hierarchy_parser(text: str):
    matches = list(re.finditer(r"^(\S.*?)$", text, re.MULTILINE))

    results = []
    for i in range(len(matches)):
        result = {"content": matches[i].groups()[0], "sub_layers": None}
        start_pos = matches[i].span()[1]
        end_pos = len(text)
        if i < len(matches) - 1:
            end_pos = matches[i + 1].span()[0]
        inner_text: str = text[start_pos:end_pos]
        inner_text = "\n".join([line[4:] for line in inner_text.splitlines()])
        if inner_text != "":
            result["sub_layers"] = recursive_4_space_hierarchy_parser(inner_text)
        results.append(result)
    return results


def hexdump_to_bytes(hexdump: str):
    hex_str = " ".join(
        re.findall(r"^[0-9a-f]{4}\s{2}([0-9a-f\s]*?)\s{3,}", hexdump, re.MULTILINE)
    )
    return bytes.fromhex(hex_str)
