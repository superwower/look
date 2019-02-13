import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { FaceDetectorComponent } from "./face-detector/face-detector.component";
import { MeComponent } from "./me/me.component";

const routes: Routes = [
  { path: "", component: FaceDetectorComponent, pathMatch: "full" },
  { path: "me", component: MeComponent, pathMatch: "full" }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
