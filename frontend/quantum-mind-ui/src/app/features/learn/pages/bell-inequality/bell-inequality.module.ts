import { NgModule } from "@angular/core";
import { BellInequalityPage } from "./bell-inequality.page";
import { BellInequalityRoutingModule } from "./bell-inequality-routing.module";
import { CommonModule } from "@angular/common";
import { SharedModule } from "../../../../shared/shared.module";

@NgModule({
  imports: [
    CommonModule,
    BellInequalityRoutingModule,
    SharedModule
  ],
  declarations: [BellInequalityPage]
})
export class BellInequalityModule { }
