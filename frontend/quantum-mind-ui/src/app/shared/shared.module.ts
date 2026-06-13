import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { EquationComponent } from "./components/equation/equation.component";

@NgModule({
  imports: [CommonModule],
  declarations: [EquationComponent],
  exports: [EquationComponent]
})
export class SharedModule {}
