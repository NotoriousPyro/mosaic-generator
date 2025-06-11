
import os
import io
import sys
import platform
import ctypes

# Windows-specific setup for libcairo-2.dll
if platform.system() == "Windows":
    cairo_dll_path = os.path.join(os.path.dirname(__file__), ".cairo")
    if not os.path.exists(cairo_dll_path):
        print("❌ ERROR: Missing '.cairo' folder. Please unzip 'windows-cairo.zip' in this directory.")
        sys.exit(1)
    try:
        os.add_dll_directory(cairo_dll_path)
        # Force early load to catch errors
        ctypes.CDLL("libcairo-2.dll")
    except AttributeError:
        # For Python < 3.8, fallback to modifying PATH (not ideal)
        os.environ["PATH"] = cairo_dll_path + os.pathsep + os.environ["PATH"]
    except OSError as e:
        print("DLL load failed:", e)
        raise

import cairosvg
from PIL import Image
import numpy as np

def load_image(input_path, size=None):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".svg":
        png_data = cairosvg.svg2png(url=input_path, output_width=size[0], output_height=size[1])
        image = Image.open(io.BytesIO(png_data))
    else:
        image = Image.open(input_path)
        if size:
            image = image.resize(size, Image.LANCZOS)

    if image.mode != "RGBA":
        image = image.convert("RGBA")

    return image

def colorize_tile(base_tile, target_color):
    tile_array = np.array(base_tile).astype(np.float32)
    r, g, b, a = tile_array[..., 0], tile_array[..., 1], tile_array[..., 2], tile_array[..., 3]

    r_norm, g_norm, b_norm = r / 255, g / 255, b / 255
    tr, tg, tb = [v / 255.0 for v in target_color]

    r_tinted = (r_norm * tr * 255).clip(0, 255)
    g_tinted = (g_norm * tg * 255).clip(0, 255)
    b_tinted = (b_norm * tb * 255).clip(0, 255)

    tinted_array = np.stack([r_tinted, g_tinted, b_tinted, a], axis=-1).astype(np.uint8)
    return Image.fromarray(tinted_array, "RGBA")

def flatten_image(image, bg_color=(255, 255, 255, 255)):
    flattened = Image.new("RGBA", image.size, bg_color)
    flattened.paste(image, mask=image.split()[-1])
    return flattened

def generate_mosaic(layout_path, output_path, grid_size=(50, 50), tile_size=(60, 60)):
    print(f"Loading layout image: {layout_path}")
    layout_img = load_image(layout_path, size=(600, 600))
    tile_img = load_image(layout_path, size=tile_size)  # Use same image as tile

    layout_flat = flatten_image(layout_img)
    tiles_x, tiles_y = grid_size
    layout_resized = layout_flat.resize((tiles_x, tiles_y), Image.LANCZOS)
    layout_np = np.array(layout_resized)

    mosaic = Image.new("RGBA", (tiles_x * tile_size[0], tiles_y * tile_size[1]))
    for y in range(tiles_y):
        for x in range(tiles_x):
            r, g, b, _ = layout_np[y, x]
            avg_color = (r, g, b)
            tinted_tile = colorize_tile(tile_img, avg_color)
            mosaic.paste(tinted_tile, (x * tile_size[0], y * tile_size[1]))

    mosaic.save(output_path)
    print(f"Mosaic saved to: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a mosaic made of the image itself.")
    parser.add_argument("input", help="Path to input image (SVG, PNG, or JPEG)")
    parser.add_argument("output", help="Path to save the output mosaic image (PNG)")
    parser.add_argument("--tiles", type=int, default=50, help="Number of tiles across and down (default 50)")
    parser.add_argument("--tile_size", type=int, default=60, help="Size of each tile in pixels (default 60)")
    args = parser.parse_args()

    # 🔄 Force output file to .png
    base, _ = os.path.splitext(args.output)
    args.output = base + ".png"

    generate_mosaic(
        layout_path=args.input,
        output_path=args.output,
        grid_size=(args.tiles, args.tiles),
        tile_size=(args.tile_size, args.tile_size)
    )
