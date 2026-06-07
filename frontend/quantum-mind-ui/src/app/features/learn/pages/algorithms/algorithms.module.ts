import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { AlgorithmsRoutingModule } from "./algorithms-routing.module";
import { AlgorithmsPage } from "./algorithms.page";

@NgModule({
  imports: [CommonModule, AlgorithmsRoutingModule],
  declarations: [AlgorithmsPage]
})
export class AlgorithmsModule {}
