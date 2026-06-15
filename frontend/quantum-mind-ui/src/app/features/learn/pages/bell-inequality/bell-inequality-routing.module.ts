import { RouterModule, Routes } from "@angular/router";
import { BellInequalityPage } from "./bell-inequality.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: BellInequalityPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BellInequalityRoutingModule {}
