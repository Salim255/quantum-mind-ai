import { CommonModule } from "@angular/common";
import { QuantumAlgosRoutingModule } from "./quantum-algos-routing.module";
import { NgModule } from "@angular/core";
import { QuantumAlgosPage } from "./quantum-algos.page";

@NgModule({
  imports: [CommonModule, QuantumAlgosRoutingModule],
  declarations: [QuantumAlgosPage]
})
export class QuantumAlgosModule{}
