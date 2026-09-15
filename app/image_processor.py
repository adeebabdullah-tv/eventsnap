from pathlib import Path

from PIL import Image, ImageEnhance


def prepare_image(image_path, output_path):
    image = Image.open(image_path).convert("RGB")

    max_size = 2000

    # Only resize large images.
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

    image = ImageEnhance.Sharpness(image).enhance(1.3)

    image.save(
        output_path,
        format="JPEG",
        quality=75,
        optimize=True,
    )

    # Use the processed image only if it is actually smaller.
    original_size = Path(image_path).stat().st_size
    processed_size = Path(output_path).stat().st_size

    if processed_size >= original_size:
        Path(output_path).unlink()
        return Path(image_path)

    return Path(output_path)