import { NgModule } from "@angular/core";
import { ClassicalLogicPage } from "./classical-logic.page";
import { CommonModule } from "@angular/common";
import { ClassicalLogicRoutingModule } from "./classical-logic-routing.module";

@NgModule({
  imports: [CommonModule, ClassicalLogicRoutingModule],
  declarations: [ClassicalLogicPage]
})
export class ClassicalLogicModule {}
