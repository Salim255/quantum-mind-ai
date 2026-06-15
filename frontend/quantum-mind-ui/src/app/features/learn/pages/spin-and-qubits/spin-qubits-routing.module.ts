import { RouterModule, Routes } from "@angular/router";
import { SpinQubitsPage } from "./spin-qubits.page";
import { NgModule } from "@angular/core";

const routes:Routes = [
  {
    path: "",
    component: SpinQubitsPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class SpinQubitsRoutingModule {}
