import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { QuantumLogicPage } from "./quantum-logic.page";
import { QuantumLogicRoutingModule } from "./quantum-logic-routing.module";

@NgModule({
  imports: [CommonModule, QuantumLogicRoutingModule],
  declarations: [QuantumLogicPage]
})
export class QuantumLogicModule {}
