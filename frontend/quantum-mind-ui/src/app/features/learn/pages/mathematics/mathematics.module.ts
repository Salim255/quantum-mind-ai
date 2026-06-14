import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { MathematicsPage } from "./mathematics.page";
import { MathematicsRoutingModule } from "./mathematics-routing.module";
import { FormsModule } from "@angular/forms";
import { CircuitsComponent } from "./components/circuits/circuits.component";
import { SharedModule } from "../../../../shared/shared.module";

@NgModule({
  imports: [
    CommonModule,
    MathematicsRoutingModule,
    FormsModule,
    SharedModule
  ],
  declarations: [MathematicsPage, CircuitsComponent]
})
export class MathematicsModule {}
