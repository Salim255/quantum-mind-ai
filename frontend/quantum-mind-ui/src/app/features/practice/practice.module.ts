import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { PracticePage } from "./practice.page";
import { PracticeRoutingModule } from "./practice-routing.module";

@NgModule({
  imports: [CommonModule, PracticeRoutingModule],
  declarations: [PracticePage],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class PracticeModule {}
