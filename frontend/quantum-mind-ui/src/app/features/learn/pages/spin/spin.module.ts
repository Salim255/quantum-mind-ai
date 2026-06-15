import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { SpinPage } from "./spin.page";
import { SpinRoutingModule } from "./spin-routing.module";

@NgModule({
  imports: [CommonModule, SpinRoutingModule],
  declarations: [SpinPage]
})
export class SpinModule {}
