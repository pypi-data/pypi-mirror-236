import os

__all__ = ["get_image_files"]


def get_image_files(dir_path: str) -> list:
    image_files = []
    valid_extensions = [".jpg", ".png", ".jpeg", ".gif", ".bmp", ".tiff"]

    for subdir, _, files in os.walk(dir_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in valid_extensions):
                rel_dir = os.path.relpath(subdir, dir_path)
                rel_file = os.path.join(rel_dir, file)
                image_files.append(rel_file)

    image_files.sort()
    return image_files
