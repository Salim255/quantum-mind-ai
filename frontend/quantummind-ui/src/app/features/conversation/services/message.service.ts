import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";
import { AnswerPayload } from "./conversation-http.service";

@Injectable({providedIn: "root"})
export class MessageService {
  private messageSubject = new BehaviorSubject<AnswerPayload | null>(null)

  setMessage(message: AnswerPayload){
    this.messageSubject.next(message)
  }

  get getMessage(): Observable<AnswerPayload | null>{
    return this.messageSubject.asObservable()
  }
}
