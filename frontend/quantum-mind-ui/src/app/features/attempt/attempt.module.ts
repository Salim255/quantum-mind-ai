import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { AttemptPage } from "./attempt.page";
import { AttemptRoutingModule } from "./attempt-routing.module";
import { CommonModule } from "@angular/common";
import { AttemptHeaderComponent } from "./components/attempt-header/attempt-header.component";
import { QuestionComponent } from "./components/question/question.component";
import { AnswerItemComponent } from "./components/answer-item/answer-item.component";
import { AttemptFooterComponent } from "./components/attempt-footer/attempt-footer.component";
import { AttemptResultComponent } from "./components/attempt-result/attempt-result.component";
import { SharedModule } from "../../shared/shared.module";
import { AttemptResultHeaderComponent } from "./components/attempt-result-header/attempt-result-header.component";

@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    AttemptRoutingModule,
  ],
  declarations: [
    AttemptResultHeaderComponent,
    AttemptResultComponent,
    AttemptFooterComponent,
    AnswerItemComponent,
    QuestionComponent,
    AttemptHeaderComponent,
    AttemptPage
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class AttemptModule {}