import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { ProgressPage } from "./progress.page";
import { ProgressRoutingModule } from "./progress-routing.module";

@NgModule({
  imports: [CommonModule, ProgressRoutingModule],
  declarations: [ProgressPage],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class ProgressModule {}
