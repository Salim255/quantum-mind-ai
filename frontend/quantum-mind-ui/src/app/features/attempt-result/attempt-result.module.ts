import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { AttemptResultPage } from "./attempt-result.page";

@NgModule({
  imports: [CommonModule, AttemptResultRoutingModule],
  declarations: [AttemptResultPage],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class AttemptResultModule {}