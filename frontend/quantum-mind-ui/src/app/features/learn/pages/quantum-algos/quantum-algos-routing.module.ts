import { RouterModule, Routes } from "@angular/router";
import { QuantumAlgosPage } from "./quantum-algos.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: QuantumAlgosPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class QuantumAlgosRoutingModule {}
