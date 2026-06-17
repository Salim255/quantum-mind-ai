import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { SpinPage } from "./spin.page";
import { SpinRoutingModule } from "./spin-routing.module";
import { SpinHomeComponent } from "./components/spin-home/spin-home.component";

@NgModule({
  imports: [CommonModule, SpinRoutingModule],
  declarations: [SpinHomeComponent, SpinPage]
})
export class SpinModule {}
