import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# Directories
FRONTEND_SAMPLE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "sample_images"))
BACKEND_SAMPLE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads", "sample_images"))

os.makedirs(FRONTEND_SAMPLE_DIR, exist_ok=True)
os.makedirs(BACKEND_SAMPLE_DIR, exist_ok=True)

def generate_fresh_apple():
    img = Image.new("RGB", (300, 300), color=(240, 245, 240))
    draw = ImageDraw.Draw(img)
    # Draw vibrant fresh red apple with slight yellow-green gradient
    draw.ellipse([50, 50, 250, 250], fill=(210, 35, 35), outline=(160, 20, 20), width=3)
    draw.ellipse([110, 40, 160, 80], fill=(235, 180, 40)) # highlight
    # Stem & leaf
    draw.rectangle([145, 25, 153, 55], fill=(90, 50, 20))
    draw.polygon([(153, 35), (185, 20), (170, 45)], fill=(40, 160, 60))
    # Smooth finish
    img = img.filter(ImageFilter.SMOOTH)
    return img

def generate_fresh_avocado():
    img = Image.new("RGB", (300, 300), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)
    # Draw dark green skin avocado
    draw.ellipse([60, 40, 240, 260], fill=(30, 75, 40), outline=(20, 50, 25), width=4)
    # Inner flesh
    draw.ellipse([80, 60, 220, 240], fill=(160, 205, 90))
    # Seed
    draw.ellipse([115, 120, 185, 190], fill=(110, 60, 30))
    return img

def generate_spoiled_produce():
    img = Image.new("RGB", (300, 300), color=(230, 230, 225))
    draw = ImageDraw.Draw(img)
    # Draw heavily discolored, browning spoiled produce
    draw.ellipse([50, 50, 250, 250], fill=(95, 60, 35), outline=(60, 35, 20), width=4)
    # Dark brown spots
    draw.ellipse([80, 90, 150, 160], fill=(50, 30, 15))
    draw.ellipse([140, 130, 210, 200], fill=(45, 25, 10))
    draw.ellipse([100, 170, 160, 220], fill=(55, 35, 20))
    # Grayish fuzzy mold spot cluster
    draw.ellipse([170, 70, 220, 120], fill=(180, 185, 180))
    draw.ellipse([180, 80, 210, 110], fill=(210, 215, 210))
    return img

def generate_fresh_spinach():
    img = Image.new("RGB", (300, 300), color=(245, 250, 245))
    draw = ImageDraw.Draw(img)
    # Draw vibrant green spinach leaves
    draw.polygon([(150, 30), (70, 120), (100, 250), (200, 250), (230, 120)], fill=(35, 165, 65))
    # Leaf veins
    draw.line([(150, 30), (150, 250)], fill=(120, 215, 140), width=4)
    draw.line([(150, 100), (90, 140)], fill=(120, 215, 140), width=3)
    draw.line([(150, 150), (210, 190)], fill=(120, 215, 140), width=3)
    return img

if __name__ == "__main__":
    samples = {
        "sample_fresh_apple.jpg": generate_fresh_apple(),
        "sample_fresh_avocado.jpg": generate_fresh_avocado(),
        "sample_spoiled_produce.jpg": generate_spoiled_produce(),
        "sample_fresh_spinach.jpg": generate_fresh_spinach(),
    }

    for name, img in samples.items():
        frontend_path = os.path.join(FRONTEND_SAMPLE_DIR, name)
        backend_path = os.path.join(BACKEND_SAMPLE_DIR, name)
        img.save(frontend_path, "JPEG")
        img.save(backend_path, "JPEG")
        print(f"Generated sample image: {name}")

    print("All sample food images created successfully!")
