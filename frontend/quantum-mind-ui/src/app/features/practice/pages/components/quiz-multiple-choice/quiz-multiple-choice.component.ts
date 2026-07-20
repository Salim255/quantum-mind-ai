import { Component, EventEmitter, Input, Output } from "@angular/core";
import { QuizAnswer } from "../../models/quiz.model";

@Component({
  selector: "app-quiz-multiple-choice",
  templateUrl: "./quiz-multiple-choice.component.html",
  styleUrls: ["./quiz-multiple-choice.component.scss"],
  standalone: false
})
export class QuizMultipleChoiceComponent {
  @Input({ required: true })
  answers!: QuizAnswer[];

  @Input()
  selectedIds: string[] = [];

  @Output()
  selectionChanged =
  new EventEmitter<string[]>();

  toggle(id: string): void {

      const exists =
          this.selectedIds.includes(id);

      const selection =
          exists
              ? this.selectedIds.filter(x => x !== id)
              : [...this.selectedIds, id];

      this.selectionChanged.emit(selection);

}
}
