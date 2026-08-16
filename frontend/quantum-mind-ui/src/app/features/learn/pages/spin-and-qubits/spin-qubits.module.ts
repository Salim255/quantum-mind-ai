import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { SpinQubitsRoutingModule } from "./spin-qubits-routing.module";
import { SpinQubitsPage } from "./spin-qubits.page";
import { SharedModule } from "../../../../shared/shared.module";

@NgModule({
  imports: [
    CommonModule,
    SpinQubitsRoutingModule,
    SharedModule
  ],
  declarations: [SpinQubitsPage]
})
export class SpinQubitsModule {}
