import { RouterModule, Routes } from "@angular/router";
import { AlgorithmsPage } from "./algorithms.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: AlgorithmsPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class AlgorithmsRoutingModule {}
