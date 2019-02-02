async function authenticate(data) {
  return new Promise(resolve => {
    setTimeout(() => {
      const user = {
        name: 'hitoshi',
      };
      resolve(user);
    }, 100);
  });
}

async function main() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const context = canvas.getContext('2d');

  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true}).then(stream => {
      video.srcObject = stream;
    });
  }
  await faceapi.loadTinyFaceDetectorModel('models');
  let timer = null;
  const run = () =>
    setInterval(async () => {
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.drawImage(video, 0, 0, 640, 480);
      const data = canvas.toDataURL();
      let result = await faceapi.detectAllFaces(
        canvas,
        new faceapi.TinyFaceDetectorOptions(),
      );
      if (result.length === 1) {
        const {box, score} = result[0];
        const {x, y, width, height} = box;
        context.beginPath();
        context.rect(x, y, width, height);
        context.stroke();
        if (score >= 0.5) {
          clearInterval(timer);
          authenticate(data).then(result => {
            alert(result.name);
          });
          timer = run();
        }
      }
    }, 100);
  timer = run();
}

main();
