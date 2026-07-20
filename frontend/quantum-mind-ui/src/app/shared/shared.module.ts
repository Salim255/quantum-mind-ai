import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { EquationComponent } from "./components/equation/equation.component";
import { PageContentAsideComponent } from "./components/page-content-aside/page-content-aside.component";
import { AndGateComponent } from "./components/and-gate/and-gate.component";
import { ScrollToDirective } from "./directives/scroll-to.directive";

@NgModule({
  imports: [CommonModule],
  declarations: [
    ScrollToDirective,
    AndGateComponent,
    PageContentAsideComponent,
    EquationComponent,
  ],
  exports: [
    ScrollToDirective,
    AndGateComponent,
    PageContentAsideComponent,
    EquationComponent,
  ]
})
export class SharedModule {}
