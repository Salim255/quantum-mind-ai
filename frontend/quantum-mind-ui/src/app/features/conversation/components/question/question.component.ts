import { Component, Input, OnDestroy, OnInit, signal } from "@angular/core";
import { QuestionService } from "../../services/question.service";
import { Subscription } from "rxjs";

@Component({
  selector: "app-question",
  templateUrl: "./question.component.html",
  styleUrl: "./question.component.scss",
  standalone: false
})

export class QuestionComponent implements OnInit, OnDestroy{
  question = signal<string | null>(null);

  private questionSubscription!: Subscription;
  constructor(private questionService: QuestionService){}

  ngOnInit(): void {
    this.subscribeToUserQuestion()
  }

  subscribeToUserQuestion(): void {
    this.questionSubscription = this.questionService.getQuestion$.subscribe(
      (question) => {
        this.question.set(question)
      }
    )
  }

  ngOnDestroy(): void {
    this.questionSubscription?.unsubscribe()
  }
}
