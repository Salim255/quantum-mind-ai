import { RouterModule, Routes } from "@angular/router";
import { QuantumComputingPage } from "./quantum-computing.page";
import { NgModule } from "@angular/core";

const routes: Routes= [
  {
      path: "",
      component: QuantumComputingPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class QuantumComputingRoutingModule {}
