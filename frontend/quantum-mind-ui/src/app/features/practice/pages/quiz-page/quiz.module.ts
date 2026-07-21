import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { QuizRoutingModule } from "./quiz-routing.module";
import { QuizPage } from "./quiz-page";
import { QuizHeaderComponent } from "./components/quiz-header/quiz-header.component";
import { QuizProgressComponent } from "./components/quiz-progress/quiz-progress.component";
import { QuizQuestionComponent } from "./components/quiz-question/quiz-question.component";
import { QuizMultipleChoiceComponent } from "./components/quiz-multiple-choice/quiz-multiple-choice.component";
import { QuizSingleChoiceComponent } from "./components/quiz-single-choic/quiz-single-choice.component";
import { QuizFooterComponent } from "./components/quiz-footer/quiz-footer.component";

@NgModule({
  imports: [QuizRoutingModule, CommonModule],
  declarations: [
    QuizFooterComponent,
    QuizFooterComponent,
    QuizSingleChoiceComponent,
    QuizMultipleChoiceComponent,
    QuizPage,
    QuizHeaderComponent,
    QuizProgressComponent,
    QuizQuestionComponent
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class QuizModule{}
