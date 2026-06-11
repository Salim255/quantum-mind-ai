import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { MathematicsPage } from "./mathematics.page";
import { MathematicsRoutingModule } from "./mathematics-routing.module";
import { FormsModule } from "@angular/forms";

@NgModule({
  imports: [CommonModule, MathematicsRoutingModule, FormsModule],
  declarations: [MathematicsPage]
})
export class MathematicsModule {}
