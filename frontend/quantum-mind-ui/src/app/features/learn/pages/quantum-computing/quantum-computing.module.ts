import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { PhysicsModule } from "../physics/physics.module";
import { QuantumComputingPage } from "./quantum-computing.page";
import { QuantumComputingRoutingModule } from "./quantum-computing-routing.module";

@NgModule({
  imports: [CommonModule, QuantumComputingRoutingModule],
  declarations: [QuantumComputingPage]
})
export class QuantumComputingModule {}
