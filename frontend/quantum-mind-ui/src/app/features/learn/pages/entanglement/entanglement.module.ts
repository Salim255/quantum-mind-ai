import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { EntanglementRoutingModule } from "./entanglement-routing.module";
import { SharedModule } from "../../../../shared/shared.module";
import { EntanglementPage } from "./entanglement.page";

@NgModule({
  imports: [
    CommonModule,
    EntanglementRoutingModule,
    SharedModule
  ],
  declarations: [EntanglementPage]
})
export class EntanglementModule {}
