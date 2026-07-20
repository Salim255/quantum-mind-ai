import { Component, EventEmitter, Input, Output } from "@angular/core";
import { QuizAnswer } from "../../models/quiz.model";

@Component({
  selector: "app-quiz-single-choice",
  templateUrl: "./quiz-single-choice.component.html",
  styleUrls: ["./quiz-single-choice.component.scss"],
  standalone: false
})
export class QuizSingleChoiceComponent {
  @Input({ required: true })
  answers!: QuizAnswer[];

  @Input()
  selectedAnswerId?: string;

  @Output()
  selected = new EventEmitter<string>();

  onSelect(id: string): void {
      this.selected.emit(id);
  }
}
