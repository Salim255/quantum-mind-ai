import { RouterModule, Routes } from "@angular/router";

import { NgModule } from "@angular/core";
import { QuantumImpactPage } from "./quantum-impact.page";

const routes: Routes = [
  {
    path: "",
    component: QuantumImpactPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class QuantumImpactRoutingModule {}
