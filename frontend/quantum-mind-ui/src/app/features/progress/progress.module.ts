import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { ProgressPage } from "./progress.page";
import { ProgressRoutingModule } from "./progress-routing.module";
import { ProgressHeaderComponent } from "./components/progress-header/progress-header.component";

@NgModule({
  imports: [CommonModule, ProgressRoutingModule],
  declarations: [
    ProgressHeaderComponent,
    ProgressPage
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class ProgressModule {}
