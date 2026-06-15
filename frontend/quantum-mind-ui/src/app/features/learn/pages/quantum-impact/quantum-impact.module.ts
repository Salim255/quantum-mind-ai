import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { QuantumImpactRoutingModule } from "./quantum-impact-routing.module";
import { QuantumImpactPage } from "./quantum-impact.page";


@NgModule({
  imports: [CommonModule, QuantumImpactRoutingModule],
  declarations: [QuantumImpactPage]
})
export class QuantumImpactModule {}
