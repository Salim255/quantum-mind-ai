import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { AttemptResultPage } from "./attempt-result.page";
import { AttemptResultRoutingModule } from "./attempt-result-routing.module";

@NgModule({
  imports: [CommonModule, AttemptResultRoutingModule],
  declarations: [AttemptResultPage],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class AttemptResultModule {}