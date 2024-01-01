const tf = require('@tensorflow/tfjs-node');
const cocoSsd = require('@tensorflow-models/coco-ssd');
const fs = require('fs');
const { createCanvas, loadImage } = require('canvas');

async function loadAndDetect() {
  // Load the COCO-SSD model
  const model = await cocoSsd.load();

  const imageBuffer = fs.readFileSync('nyc.jpg');

  // Decode the image using tf.node.decodeImage
  const decodedImage = tf.node.decodeImage(imageBuffer);

  // Detect objects in the image
  const predictions = await model.detect(decodedImage);

  // Print the detected objects
  console.log('Detected objects:');
  predictions.forEach((prediction) => {
    console.log(`${prediction.class} (${Math.round(prediction.score * 100)}% confidence)`);
  });

  // Create a new canvas and get its context
  const canvas = createCanvas(decodedImage.shape[1], decodedImage.shape[0]);
  const ctx = canvas.getContext('2d');

  // Set the font size
  ctx.font = '20px Arial';

  // Load the image into the canvas
  const img = await loadImage(imageBuffer);
  ctx.drawImage(img, 0, 0);

  // Draw a red bordered bounding box for each detected object
  predictions.forEach((prediction) => {
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 5;
    ctx.strokeRect(
      prediction.bbox[0],
      prediction.bbox[1],
      prediction.bbox[2],
      prediction.bbox[3]
    );

    // Calculate the position for the label
    const text = `${prediction.class} (${Math.round(prediction.score * 100)}%)`;
    const textWidth = ctx.measureText(text).width;
    const labelX = prediction.bbox[0] + prediction.bbox[2] - textWidth;
    const labelY = prediction.bbox[1];

    // Set the fill style to red and draw a filled rectangle
    ctx.fillStyle = 'red';
    ctx.fillRect(labelX, labelY - 30, textWidth, 30);

    // Set the fill style to white and draw the label text
    ctx.fillStyle = 'white';
    ctx.fillText(
      text,
      labelX,
      labelY - 10
    );
  });

  // Save the canvas as an image
  const out = fs.createWriteStream('output.png');
  const stream = canvas.createPNGStream();
  stream.pipe(out);
  out.on('finish', () => console.log('Annotated image saved as output.png'));
}

loadAndDetect();