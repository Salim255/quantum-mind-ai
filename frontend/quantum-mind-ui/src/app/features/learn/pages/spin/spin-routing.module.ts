import { RouterModule, Routes } from "@angular/router";
import { SpinPage } from "./spin.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: SpinPage

  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SpinRoutingModule {}
