import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { AttemptPage } from "./attempt.page";
import { AttemptRoutingModule } from "./attempt-routing.module";
import { CommonModule } from "@angular/common";

@NgModule({
  imports: [
    CommonModule,
    AttemptRoutingModule,
  ],
  declarations: [AttemptPage],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class AttemptModule {}