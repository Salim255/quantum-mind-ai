import { RouterModule, Routes } from "@angular/router";
import { ClassicalLogicPage } from "./classical-logic.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: ClassicalLogicPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ClassicalLogicRoutingModule {}
