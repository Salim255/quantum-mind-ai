import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { EquationComponent } from "./components/equation/equation.component";
import { PageContentAsideComponent } from "./components/page-content-aside/page-content-aside.component";
import { AndGateComponent } from "./components/and-gate/and-gate.component";

@NgModule({
  imports: [CommonModule],
  declarations: [AndGateComponent, PageContentAsideComponent, EquationComponent],
  exports: [AndGateComponent, PageContentAsideComponent, EquationComponent]
})
export class SharedModule {}
