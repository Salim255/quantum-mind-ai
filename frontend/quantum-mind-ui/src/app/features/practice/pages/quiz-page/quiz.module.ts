import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { QuizRoutingModule } from "./quiz-routing.module";
import { QuizPage } from "./quiz-page";
import { QuizHeaderComponent } from "../components/quiz-header/quiz-header.component";
import { QuizProgressComponent } from "../components/quiz-progress/quiz-progress.component";
import { QuizQuestionComponent } from "../components/quiz-question/quiz-question.component";
import { QuizMultipleChoiceComponent } from "../components/quiz-multiple-choice/quiz-multiple-choice.component";

@NgModule({
  imports: [QuizRoutingModule, CommonModule],
  declarations: [
    QuizMultipleChoiceComponent,
    QuizPage,
    QuizHeaderComponent,
    QuizProgressComponent,
    QuizQuestionComponent
  ],

})
export class QuizModule{}
