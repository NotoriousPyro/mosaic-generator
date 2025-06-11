
# Self Mosaic Generator 🧩
Turn any image (PNG, JPEG, or SVG) into a beautiful **mosaic made of smaller tinted versions of itself**.

### Donate
BTC: bc1qhwzln2zclq9lycnr300pvcxd3nx6my7ha7clq6

SOL: 9dxtJ8xJEWVeFv75eQ288ESKfofvfMrQBixyBHF6K54f

## 🖼️ What It Does
Given an input image, this script:
- Uses the image itself as a **repeating tile**
- Matches each tile's color to the corresponding region in the original
- Produces a stylized mosaic that recreates the image using itself

## Examples

### Tiled "my honest reacton" meme
```bash
> python.exe self_mosaic_generator.py "my honest reaction.png" "my honest reaction-tiled.png"
```

Input:

<img src="images/my honest reaction.png" alt="Alt text" width="300"/>

Output:

<img src="images/my honest reaction-tiled.png" alt="Alt text" width="300"/>

### Tiled laugh emoji

```bash
> python.exe self_mosaic_generator.py "laugh.svg" "laugh-tiled.png"
```

Input:

<img src="images/laugh.svg" alt="Alt text" width="300"/>

Output:

<img src="images/laugh-tiled.png" alt="Alt text" width="300"/>

---

## 🔧 Requirements

You’ll need:

- Python 3.7+
- The following Python packages:

```
pip install -r requirements.txt
```

### `requirements.txt`
```
Pillow>=9.0.0
cairosvg>=2.5.0
numpy>=1.20.0
```

---
## 🪟 Windows Setup Guide

### 🔁 Quick Setup

If you're on Windows:

1. Locate the file `cairo-windows.zip` included with this repo.
2. Unzip it — it will create a `.cairo/` folder:
   ```
   mosaic-generator/
   ├── self_mosaic_generator.py
   ├── requirements.txt
   ├── windows-cairo.zip
   ├── .cairo/
   │   ├── libcairo-2.dll
   │   ├── ...
   ```

3. Run the script:
   ```bash
   python self_mosaic_generator.py input.jpg output.png --tiles 60 --tile_size 60
   ```

> ⚠️ If you forget to unzip `windows-cairo.zip`, the script will warn you and exit.

---

## 🐧 Linux Setup Guide

Most distros already include Cairo. If not:

```bash
sudo apt update
sudo apt install libcairo2
```

Then install Python dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

### Command-line usage:

```bash
python self_mosaic_generator.py input_image.svg output_mosaic.png --tiles 60 --tile_size 60
```

### Arguments:

| Argument      | Description                              | Default  |
|---------------|------------------------------------------|----------|
| `input`       | Path to input image (PNG, JPEG, SVG)     | *(required)* |
| `output`      | Path to save final mosaic (PNG recommended) | *(required)* |
| `--tiles`     | Number of tiles across and down          | 50       |
| `--tile_size` | Pixel size of each tile (width = height) | 60       |

---

## 🧪 Example

```bash
python self_mosaic_generator.py discord_logo.svg discord_mosaic.png --tiles 60 --tile_size 64
```

This will produce a 3840×3840 image (60×64 tiles).

---

## 📌 Notes

- The input image is automatically flattened onto a white background to avoid black halos from transparency.
- Works best with **square images** or when scaled before use.
- SVG input is rendered with `cairosvg`, so make sure GTK/Cairo is properly installed (see above).

---

## 📬 Questions?

Drop me a note or fork the repo to experiment. Enjoy creating recursive, self-referential mosaics!


## 🧾 Third-Party Licenses

This project includes compiled shared libraries for Windows inside `cairo-windows.zip`.

All third-party libraries (e.g. Cairo, FreeType, HarfBuzz, Fontconfig, Brotli) are open-source and redistributed under their respective licenses, which are included in the `.cairo/` folder after unzipping.

See the included `LICENSE-*.txt` files in `.cairo/` for details.