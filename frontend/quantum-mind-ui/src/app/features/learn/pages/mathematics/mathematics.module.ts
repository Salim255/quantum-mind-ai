import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { MathematicsPage } from "./mathematics.page";
import { MathematicsRoutingModule } from "./mathematics-routing.module";
import { FormsModule } from "@angular/forms";
import { CircuitsComponent } from "./components/circuits/circuits.component";

@NgModule({
  imports: [CommonModule, MathematicsRoutingModule, FormsModule],
  declarations: [MathematicsPage, CircuitsComponent]
})
export class MathematicsModule {}
