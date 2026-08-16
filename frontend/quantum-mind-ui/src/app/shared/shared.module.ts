import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { EquationComponent } from "./components/equation/equation.component";
import { PageContentAsideComponent } from "./components/page-content-aside/page-content-aside.component";
import { AndGateComponent } from "./components/and-gate/and-gate.component";
import { ScrollToDirective } from "./directives/scroll-to.directive";
import { AngularSplitModule } from "angular-split";
import { SplitPanelComponent } from "./kits/split-panel/split-panel.component";

@NgModule({
  imports: [AngularSplitModule, CommonModule],
  declarations: [
    SplitPanelComponent,
    ScrollToDirective,
    AndGateComponent,
    PageContentAsideComponent,
    EquationComponent,
  ],
  exports: [
    SplitPanelComponent,
    ScrollToDirective,
    AndGateComponent,
    PageContentAsideComponent,
    EquationComponent,
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class SharedModule {}
