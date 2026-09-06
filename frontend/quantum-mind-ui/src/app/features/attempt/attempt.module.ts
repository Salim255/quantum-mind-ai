import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { AttemptPage } from "./attempt.page";
import { AttemptRoutingModule } from "./attempt-routing.module";
import { CommonModule } from "@angular/common";
import { AttemptHeaderComponent } from "./components/attempt-header/attempt-header.component";
import { QuestionComponent } from "./components/question/question.component";

@NgModule({
  imports: [
    CommonModule,
    AttemptRoutingModule,
  ],
  declarations: [
    QuestionComponent,
    AttemptHeaderComponent,
    AttemptPage
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class AttemptModule {}