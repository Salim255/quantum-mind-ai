import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { QuantumImpactRoutingModule } from "./quantum-impact-routing.module";
import { QuantumImpactPage } from "./quantum-impact.page";
import { SharedModule } from "../../../../shared/shared.module";


@NgModule({
  imports: [
    CommonModule,
    QuantumImpactRoutingModule,
    SharedModule
  ],
  declarations: [QuantumImpactPage]
})
export class QuantumImpactModule {}
