import { CommonModule, NgComponentOutlet } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { EquationComponent } from "./components/equation/equation.component";
import { PageContentAsideComponent } from "./components/page-content-aside/page-content-aside.component";
import { AndGateComponent } from "./components/and-gate/and-gate.component";
import { ScrollToDirective } from "./directives/scroll-to.directive";
import { AngularSplitModule } from "angular-split";
import { SplitPanelComponent } from "./kits/split-panel/split-panel.component";
import { AppOverlayComponent } from "./kits/app-overlay/app-overlay.component";
import { ModalComponent } from "./kits/modal/ modal.component";

@NgModule({
  imports: [
     NgComponentOutlet,
    AngularSplitModule,
    CommonModule
  ],
  declarations: [
    ModalComponent, 
    AppOverlayComponent,
    SplitPanelComponent,
    ScrollToDirective,
    AndGateComponent,
    PageContentAsideComponent,
    EquationComponent,
  ],
  exports: [
    ModalComponent,
    AppOverlayComponent,
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
