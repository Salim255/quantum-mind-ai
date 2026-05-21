import { Injectable } from "@angular/core";
import { ConversationHttpService, ConversationPayload } from "./conversation-http.service";
import { BehaviorSubject, Observable } from "rxjs";
import { Conversation } from "../model/conversation.model";


@Injectable({providedIn: "root"})
export class ConversationService {
  private conversationSubject = new BehaviorSubject<Conversation| null>(null)
  constructor(private conversationHttpService: ConversationHttpService){}

  sendMessage(payload: ConversationPayload): Observable<any>{
    return this.conversationHttpService.sendMessage(payload);
  }

  setConversation(conversation: Conversation){
    this.conversationSubject.next(conversation);
  }

  get getConversation(): Observable<Conversation | null> {
    return this.conversationSubject.asObservable();
  }
  appendMessage(){

  }
}
