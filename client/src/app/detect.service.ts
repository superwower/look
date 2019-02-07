import { Injectable } from "@angular/core";

@Injectable({
  providedIn: "root"
})
export class DetectService {
  constructor() {
    await faceapi.loadTinyFaceDetectorModel("assets/models");
  }

  async detect(canvas): void {
    let result = await faceapi.detectAllFaces(
      canvas,
      new faceapi.TinyFaceDetectorOptions()
    );
  }
}
