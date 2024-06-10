import bboxes from "./images/bboxes.json";

(() => {
  const centerToImageMap = new Map<[number, number], string>();
  for (const [image, image_boxes] of Object.entries(bboxes)) {
    for (const box of image_boxes) {
      centerToImageMap.set([box[0]!, box[1]!], image);
    }
  }

  function getClosestImage(x: number, y: number) {
    let minDistance = Number.MAX_VALUE;
    let image = "";
    for (const mapElement of centerToImageMap) {
      const imageX = mapElement[0][0];
      const imageY = mapElement[0][1];

      // Ignore sqrt for performance
      const distance = (imageX - x) ** 2 + (imageY - y) ** 2;
      if (distance < minDistance) {
        minDistance = distance;
        image = mapElement[1];
      }
    }

    return image;
  }

  const div = document.getElementById("background") as HTMLDivElement;

  window.addEventListener("click", (event) => {
    div.innerText = "";

    document.body.style.cursor = "wait";
    const image = getClosestImage(
      event.clientX / window.innerWidth,
      event.clientY / window.innerHeight,
    );
    document.body.style.cursor = "default";

    div.style.backgroundImage = `url(/src/images/augmented/${image})`;
  });
})();
