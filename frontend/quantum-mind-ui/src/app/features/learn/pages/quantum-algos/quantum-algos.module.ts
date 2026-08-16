import { CommonModule } from "@angular/common";
import { QuantumAlgosRoutingModule } from "./quantum-algos-routing.module";
import { NgModule } from "@angular/core";
import { QuantumAlgosPage } from "./quantum-algos.page";
import { SharedModule } from "../../../../shared/shared.module";

@NgModule({
  imports: [
    CommonModule,
    QuantumAlgosRoutingModule,
    SharedModule
  ],
  declarations: [QuantumAlgosPage]
})
export class QuantumAlgosModule{}
