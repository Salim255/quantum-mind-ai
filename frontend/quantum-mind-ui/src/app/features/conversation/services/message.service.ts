import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";
import { AnswerPayload } from "./conversation-http.service";

@Injectable({providedIn: "root"})
export class MessageService {
  private streamingResponseSubject = new BehaviorSubject<string | null>(null)
  private messageSubject = new BehaviorSubject<AnswerPayload | null>(null)

  constructor(){}


  get getStreamResponse$(): Observable<string | null>{
    return this.streamingResponseSubject.asObservable();
  }

  get getMessage$(): Observable<AnswerPayload | null>{
    return this.messageSubject.asObservable()
  }


}
