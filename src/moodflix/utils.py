import base64
from pathlib import Path


def img_to_bytes(img_path):
    """Converts an image to bytes"""
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, size):
    """Converts an image to HTML"""
    return f"<img src='data:image/png;base64,{img_to_bytes(img_path)}' class='img-fluid' width='{size}'>"


def center_html(flag, obj):
    """Centers an object in HTML"""
    return f"<{flag} style='text-align: center;'>{obj}</{flag}>"
