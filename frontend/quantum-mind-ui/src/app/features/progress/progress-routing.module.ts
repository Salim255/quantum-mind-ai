import { RouterModule, Routes } from "@angular/router";
import { ProgressPage } from "./progress.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: ProgressPage
  }
]

  NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })

  export class ProgressRoutingModule {}
