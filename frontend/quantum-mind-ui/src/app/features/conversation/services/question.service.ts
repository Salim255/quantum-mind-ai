import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({providedIn: "root"})
export class QuestionService {
  private questionSubject = new BehaviorSubject<string | null>(this.loadFromSession());

  constructor(){}




  private saveToSession(query: string) {
    sessionStorage.setItem('currentQuestion', JSON.stringify(query));
  }

  private loadFromSession(): string | null {
    const data = sessionStorage.getItem('currentQuestion');
    return data ? JSON.parse(data) : null;
  }
}
