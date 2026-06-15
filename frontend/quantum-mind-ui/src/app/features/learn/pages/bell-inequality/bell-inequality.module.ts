import { NgModule } from "@angular/core";
import { BellInequalityPage } from "./bell-inequality.page";
import { BellInequalityRoutingModule } from "./bell-inequality-routing.module";
import { CommonModule } from "@angular/common";

@NgModule({
  imports: [CommonModule, BellInequalityRoutingModule],
  declarations: [BellInequalityPage]
})
export class BellInequalityModule { }
