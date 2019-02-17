import { Component, OnInit } from '@angular/core'

import { Face } from '../face'
import { AuthService } from '../auth.service'

enum UploadStatus {
  Nothing,
  Pending,
  Successful,
  Fail,
}

@Component({
  selector: 'app-me',
  templateUrl: './me.component.html',
  styleUrls: ['./me.component.scss'],
})
export class MeComponent implements OnInit {
  faces: Face[] = []
  _uploadStatus: UploadStatus = UploadStatus.Nothing

  constructor(private authService: AuthService) {}

  deleteFace(id: number): void {
    if (!confirm('Are you sure?')) {
      return
    }
    this.authService.deleteFace(id).subscribe(() => {
      alert('Deleted')
    })
  }

  registerFace(imageInput: any): void {
    const file: File = imageInput.files[0]
    this._uploadStatus = UploadStatus.Pending
    this.authService.registerFace(file).subscribe(
      () => {
        this._uploadStatus = UploadStatus.Successful
      },
      () => {
        this._uploadStatus = UploadStatus.Fail
      }
    )
  }

  ngOnInit() {}

  get uploadStatus(): string {
    switch (this._uploadStatus) {
      case UploadStatus.Nothing:
        return ''
      case UploadStatus.Pending:
        return 'Uploading image...'
      case UploadStatus.Successful:
        return 'Uploaded'
      case UploadStatus.Fail:
        return 'Failed'
      default:
        throw new Error('Unexpected upload status value' + this._uploadStatus)
    }
  }
}
