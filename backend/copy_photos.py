import os
import shutil
import glob

artifact_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "brain", "11fc7c50-3dcb-435f-8fdb-a2bc10506133"))
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "sample_images"))
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads", "sample_images"))

os.makedirs(frontend_dir, exist_ok=True)
os.makedirs(backend_dir, exist_ok=True)

mapping = {
    "sample_fresh_apple": "sample_fresh_apple.jpg",
    "sample_fresh_avocado": "sample_fresh_avocado.jpg",
    "sample_spoiled_produce": "sample_spoiled_produce.jpg",
    "sample_fresh_spinach": "sample_fresh_spinach.jpg"
}

for key, target_name in mapping.items():
    matches = glob.glob(os.path.join(artifact_dir, f"{key}_*.jpg"))
    if matches:
        latest = sorted(matches)[-1]
        dest1 = os.path.join(frontend_dir, target_name)
        dest2 = os.path.join(backend_dir, target_name)
        shutil.copy(latest, dest1)
        shutil.copy(latest, dest2)
        print(f"Copied {os.path.basename(latest)} -> {target_name}")
    else:
        print(f"No file found for {key}")

print("Real food photography images deployed successfully!")
