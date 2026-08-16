import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { QuantumLogicPage } from "./quantum-logic.page";
import { QuantumLogicRoutingModule } from "./quantum-logic-routing.module";
import { SharedModule } from "../../../../shared/shared.module";

@NgModule({
  imports: [
    CommonModule,
    QuantumLogicRoutingModule,
    SharedModule
  ],
  declarations: [QuantumLogicPage]
})
export class QuantumLogicModule {}
