import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { SpinPage } from "./spin.page";
import { SpinRoutingModule } from "./spin-routing.module";
import { SpinHomeComponent } from "./components/spin-home/spin-home.component";
import { QuantumClockComponent } from "./components/quantum-clock/quantum-clock.component";
import { SamDirectionComponent } from "./components/same-direction/same-direction.component";
import { DifferentDirectionComponent } from "./components/different-direction/different-direction.component";
import { MeasurementComponent } from "./components/measurement/measurement.component";

@NgModule({
  imports: [CommonModule, SpinRoutingModule],
  declarations: [
    MeasurementComponent,
    DifferentDirectionComponent,
    SamDirectionComponent,
    QuantumClockComponent,
    SpinHomeComponent,
    SpinPage,
  ]
})
export class SpinModule {}
