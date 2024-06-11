import bboxes from "./images/bboxes.json";
import { Peter } from "./peter";

(() => {
  const centerToImageMap = new Map<[number, number], string>();
  for (const [image, image_boxes] of Object.entries(bboxes)) {
    for (const box of image_boxes) {
      centerToImageMap.set([box[0]!, box[1]!], image);
    }
  }

  function getClosestImage(mouseX: number, mouseY: number) {
    let minDistance = Number.MAX_VALUE;
    let closestImage = "";
    for (const [[bboxCenterX, bboxCenterY], image] of centerToImageMap) {
      // Ignore sqrt for performance
      const distance =
        (mouseX - bboxCenterX) ** 2 + (mouseY - bboxCenterY) ** 2;
      if (distance < minDistance) {
        minDistance = distance;
        closestImage = image;
      }
    }

    return closestImage;
  }

  const div = document.getElementById("oat-milkers") as Peter;

  window.addEventListener("click", (event) => {
    div.innerText = "";

    document.body.style.cursor = "wait";
    const image = getClosestImage(
      event.clientX / window.innerWidth,
      event.clientY / window.innerHeight,
    );
    document.body.style.cursor = "default";

    div.style.backgroundImage = `url(/images/augmented/${image})`;
  });
})();
