import os
from pathlib import Path

from PIL import Image
from ultralytics import YOLO
from ultralytics.engine.results import Boxes

IMAGE_HEIGHT = 1080
IMAGE_WIDTH = 1920


def resize_images(data_dir: Path, target_width=IMAGE_WIDTH, target_height=IMAGE_HEIGHT):
    output_dir = data_dir / "resized"
    os.makedirs(output_dir, exist_ok=True)

    for i, image in enumerate(data_dir.glob("*.jpg")):
        image = Image.open(image)
        image = image.resize((target_width, target_height))
        image.save(output_dir / f"{i}.jpg", quality=95)


def get_bbox_centers(boxes: Boxes):
    """Gets the centers of any bounding boxes in the image."""
    centers = [
        (
            (round(((box[0] + box[2]) / 2).item(), 5)),
            round(((box[1] + box[3]) / 2).item(), 5),
        )
        for box in boxes.xyxyn
    ]

    return centers


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--data-dir", help="Data dir containing images", required=True
    )

    args = parser.parse_args()
    data_dir = Path(args.data_dir)

    resized_dir = data_dir / "resized"
    if not resized_dir.exists():
        resize_images(data_dir)

    model = YOLO()

    # Class 8 = 'boat'
    results = model(source=resized_dir, classes=[8], stream=True)

    outfile = data_dir / "bboxes.txt"

    # Remove existing bboxes file
    try:
        os.remove(outfile)
    except FileNotFoundError:
        pass

    with open(outfile, "a") as f:
        for i, result in enumerate(results):
            if not result:
                continue

            centers = get_bbox_centers(result.boxes)
            for center in centers:
                (x, y) = center
                f.write(f"{Path(result.path).name}: {x},{y}\n")
