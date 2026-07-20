import { Component, EventEmitter, Input, Output } from "@angular/core";
import { QuizQuestion } from "../../models/quiz.model";

@Component({
  selector: "app-quiz-question",
  templateUrl: "./quiz-question.component.html",
  styleUrls: ["./quiz-question.component.scss"],
  standalone: false
})
export class QuizQuestionComponent {
  @Input({ required: true })
  question!: QuizQuestion;

  @Input()
  selectedAnswerId?: string;

  @Input()
  selectedIds: string[] = [];

  @Output()
  answerSelected =
  new EventEmitter<string>();

  @Output()
  selectionChanged =
  new EventEmitter<string[]>();
}
