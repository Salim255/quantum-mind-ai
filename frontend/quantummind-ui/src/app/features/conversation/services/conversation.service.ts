import { Injectable } from "@angular/core";
import { ConversationHttpService, ConversationPayload } from "./conversation-http.service";
import { BehaviorSubject, Observable } from "rxjs";


export interface MessageSchema {
  question: string;
  response: any;
}
export interface ConversationSchema {
  user_id: string;
  conversation_id: string;
  messages: MessageSchema []
}

@Injectable({providedIn: "root"})
export class ConversationService {
  private conversationSubject = new BehaviorSubject<ConversationSchema | null>(null)
  constructor(private conversationHttpService: ConversationHttpService){}

  sendMessage(payload: ConversationPayload): Observable<any>{
    return this.conversationHttpService.sendMessage(payload);
  }

  setConversation(conversation: ConversationSchema){
    this.conversationSubject.next(conversation);
  }

  get getConversation() {
    return this.conversationSubject.asObservable();
  }
  appendMessage(){

  }
}
