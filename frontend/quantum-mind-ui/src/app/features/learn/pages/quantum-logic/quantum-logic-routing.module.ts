import { RouterModule, Routes } from "@angular/router";
import { NgModule } from "@angular/core";
import { QuantumLogicPage } from "./quantum-logic.page";

const routes: Routes= [
  {
      path: "",
      component: QuantumLogicPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class QuantumLogicRoutingModule {}
