import json
import os
from pathlib import Path

import Augmentor
from ultralytics import YOLO
from ultralytics.engine.results import Boxes

TARGET_IMAGE_HEIGHT = 1080
TARGET_IMAGE_WIDTH = 1920


def augment_images(
    source_dir: Path,
    output_dir,
    target_width=TARGET_IMAGE_WIDTH,
    target_height=TARGET_IMAGE_HEIGHT,
) -> None:
    p = Augmentor.Pipeline(source_directory=source_dir, output_directory=output_dir)
    p.flip_left_right(probability=0.5)
    p.rotate(probability=1.0, max_left_rotation=5, max_right_rotation=5)
    p.crop_random(probability=0.25, percentage_area=0.5)
    p.skew_left_right(probability=0.5, magnitude=0.4)
    p.resize(probability=1.0, width=target_width, height=target_height)
    p.sample(1000)


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


def build_image_to_bounding_boxes(
    augmented_dir: Path,
) -> dict[str, list[tuple[float, float]]]:
    """Use YOLO to find the center of each ship/boat within each image.

    :return: A dictionary mapping image names to a list of centers of the bounding boxes.
    """
    model = YOLO()

    # Class 8 = 'boat'
    results = model(source=augmented_dir, classes=[8], stream=True, conf=0.6)

    result_dict = {}
    image_index = 0

    for result in results:
        if not result:
            os.remove(result.path)
            continue

        centers = get_bbox_centers(result.boxes)

        # Change the crazy augmentor output names to 0 based index names
        image_path = Path(result.path)
        new_path = image_path.parent / f"{image_index}.jpg"
        Path.rename(image_path, new_path)
        result_dict[new_path.name] = centers
        image_index += 1

    return result_dict


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--data-dir", help="Data directory containing images", required=True
    )
    parser.add_argument(
        "-s", "--save-dir", help="Directory to save augmented images", required=False
    )

    args = parser.parse_args()
    data_dir = Path(args.data_dir)

    if not args.save_dir:
        augmented_dir = data_dir / "augmented"
    else:
        augmented_dir = Path(args.save_dir)

    if not augmented_dir.exists():
        os.makedirs(augmented_dir, exist_ok=True)
        augment_images(data_dir, augmented_dir)

    image_to_bounding_box_dict = build_image_to_bounding_boxes(augmented_dir)
    outfile = data_dir / "bboxes.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(image_to_bounding_box_dict, f, ensure_ascii=False, indent=4)
