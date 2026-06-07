import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { MathematicsPage } from "./mathematics.page";
import { MathematicsRoutingModule } from "./mathematics-routing.module";

@NgModule({
  imports: [CommonModule, MathematicsRoutingModule],
  declarations: [MathematicsPage]
})
export class MathematicsModule {}
