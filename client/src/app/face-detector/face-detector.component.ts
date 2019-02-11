import { Component, OnInit, ViewChild } from "@angular/core";
import * as faceapi from "face-api.js";

import { AuthService } from "../auth.service";

@Component({
  selector: "app-face-detector",
  templateUrl: "./face-detector.component.html",
  styleUrls: ["./face-detector.component.scss"]
})
export class FaceDetectorComponent implements OnInit {
  @ViewChild("canvas") canvasDom;
  @ViewChild("video") videoDom;

  private hasCamera: boolean = false;
  private context: string;
  private authenticated: boolean = false;
  constructor(private authService: AuthService) {}

  async ngOnInit() {
    const canvas = this.canvasDom.nativeElement;
    const context = canvas.getContext("2d");
    let video;

    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true
        });
        video = this.videoDom.nativeElement;
        video.srcObject = stream;
        this.hasCamera = true;
      }
    } catch (e) {
      alert("カメラを認識できませんでした");
      return;
    }
    await faceapi.loadTinyFaceDetectorModel("assets/models");
    let timer = null;
    const run = () =>
      setInterval(async () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(video, 0, 0, 640, 480);
        const data = canvas.toDataURL();
        let result = await faceapi.detectAllFaces(
          canvas,
          new faceapi.TinyFaceDetectorOptions()
        );
        if (result.length === 1) {
          const { box, score } = result[0];
          const { x, y, width, height } = box;
          context.beginPath();
          context.rect(x, y, width, height);
          context.stroke();
          if (score >= 0.5) {
            clearInterval(timer);
            this.authService.authenticate(data).subscribe(result => {
              if (result.error) {
                alert(result.error);
              } else {
                alert(result.name);
                this.authenticated = true;
              }
              timer = run();
            });
          }
        }
      }, 2000);
    timer = run();
  }
}
