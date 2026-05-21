import { Injectable } from "@angular/core";
import { AnswerPayload, ConversationHttpService, ConversationPayload, ConversationResponse, FinalAnswer } from "./conversation-http.service";
import { BehaviorSubject, Observable, of, tap } from "rxjs";
import { Conversation } from "../model/conversation.model";
import { MessageService } from "./message.service";


@Injectable({providedIn: "root"})
export class ConversationService {
  private conversationSubject = new BehaviorSubject<Conversation| null>(null);

  constructor(
    private messageService: MessageService,
    private conversationHttpService: ConversationHttpService,
  ){}

  sendMessage(payload: ConversationPayload): Observable<ConversationResponse>{
    return this.conversationHttpService.sendMessage(payload).pipe(
      tap((response: ConversationResponse) => {
        const final_answer: FinalAnswer = response?.data.answer?.final_answer;
        const answer_payload: AnswerPayload = response.data.answer;
        this.messageService.setMessage(answer_payload);
      })
    );
  }

  setConversation(conversation: Conversation){
    this.conversationSubject.next(conversation);
  }

  fetChConversation():Observable<Conversation>{
    const conversation = new Conversation(
            'conv-1',
              'user-1',
              []
            );

    return of(conversation).pipe(
      tap((conversation: Conversation) => {
        this.setConversation(conversation);
      })
    );
  }

  get getConversation(): Observable<Conversation | null> {
    return this.conversationSubject.asObservable();
  }
  appendMessage(){}
}
