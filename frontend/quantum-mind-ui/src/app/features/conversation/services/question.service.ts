import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({providedIn: "root"})
export class QuestionService {
  private questionSubject = new BehaviorSubject<string | null>(null);

  constructor(){}

  setQuestion(question: string): void{
    this.questionSubject.next(question);
  }

  get getQuestion$(): Observable<string | null>{
    return this.questionSubject.asObservable()
  }
}
