import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { EquationComponent } from "./components/equation/equation.component";
import { PageContentAsideComponent } from "./components/page-content-aside/page-content-aside.component";

@NgModule({
  imports: [CommonModule],
  declarations: [PageContentAsideComponent, EquationComponent],
  exports: [PageContentAsideComponent, EquationComponent]
})
export class SharedModule {}
