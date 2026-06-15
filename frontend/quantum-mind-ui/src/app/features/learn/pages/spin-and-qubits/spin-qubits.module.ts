import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { SpinQubitsRoutingModule } from "./spin-qubits-routing.module";
import { SpinQubitsPage } from "./spin-qubits.page";

@NgModule({
  imports: [CommonModule, SpinQubitsRoutingModule],
  declarations: [SpinQubitsPage]
})
export class SpinQubitsModule {}
