import { Component, EventEmitter, Input, Output } from "@angular/core";

@Component({
  selector: "app-quiz-footer",
  templateUrl: "./quiz-footer.component.html",
  styleUrls: ["./quiz-footer.component.scss"],
  standalone: false
})
export class QuizFooterComponent {
  @Input()
  canGoPrevious = false;


  @Input()
  canCheck = false;


  @Input()
  canGoNext = false;



  @Output()
  previous = new EventEmitter<void>();


  @Output()
  check = new EventEmitter<void>();


  @Output()
  next = new EventEmitter<void>();

  @Input() currentQuestion = 0;

  @Input() totalQuestions = 0;
}
