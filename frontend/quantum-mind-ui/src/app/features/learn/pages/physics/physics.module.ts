import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { PhysicsRoutingModule } from "./physics-routing.module";
import { PhysicsPage } from "./physics.page";

@NgModule({
  imports: [CommonModule, PhysicsRoutingModule],
  declarations: [PhysicsPage]
})
export class PhysicsModule {}
