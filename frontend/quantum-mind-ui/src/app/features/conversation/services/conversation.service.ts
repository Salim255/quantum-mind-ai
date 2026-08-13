import { Injectable } from "@angular/core";
import {
  AnswerPayload,
  ConversationHttpService,
  ConversationPayload,
  ConversationResponse
} from "./conversation-http.service";
import { BehaviorSubject, Observable, of, tap } from "rxjs";
import { Conversation } from "../model/conversation.model";
import { MessageService } from "./message.service";
import { QuestionService } from "./question.service";
import { AssistantMessage } from "../../ai-assistant/components/assistant-message/assistant-message.component";

@Injectable({providedIn: "root"})
export class ConversationService {
  private conversationSubject = new BehaviorSubject<Conversation| null>(null);

  constructor(
    private questionService: QuestionService,
    private messageService: MessageService,
    private conversationHttpService: ConversationHttpService,
  ){}

  sendMessage(payload: ConversationPayload): Observable<ConversationResponse>{

    this.questionService.setQuestion(payload.message);
    return this.conversationHttpService.sendMessage(payload).pipe(
      tap((response: ConversationResponse) => {
        const answer_payload: AnswerPayload = response.data.answer;
        this.messageService.setMessage(answer_payload);
      })
    );
  }

  private createUserMessage(
    payload: ConversationPayload
  ): AssistantMessage {

    return {
      id: crypto.randomUUID(),
      conversationId: payload.conversation_id,
      role: "user",
      content: payload.message,
      createdAt: new Date(),
    };
  }


  private createAssistantMessage(
    conversationId: string
  ): AssistantMessage {

    return {
      id: crypto.randomUUID(),
      conversationId,
      role: "assistant",
      content: "",
      createdAt: new Date(),
    };
  }

  sendStreamMessage(payload: ConversationPayload): void {
    this.questionService.setQuestion(payload.message);
    //1 Create user message
    const userMessage = this.createUserMessage(payload);

    //2 Create assistant message
    const assistantMessage = this.createAssistantMessage(payload.conversation_id);

    this.appendMessage(userMessage);
    this.appendMessage(assistantMessage);

    this.conversationHttpService
    .sendStreamMessage(payload)
    .subscribe({
      next: (chunk: string) => {

        this.messageService.setStreamResponseSubject(chunk);
      },
      error: (err) => {console.log(err)},
      complete: () => {}
    });
  }

  setConversation(conversation: Conversation){
    this.conversationSubject.next(conversation);
  }

  fetChConversation():Observable<Conversation>{
    const conversation = new Conversation(
            'conv-1',
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

  getCurrentConversation(): Conversation | null{
    return this.conversationSubject.value;
  }

  appendMessage(payload: AssistantMessage){
    const conversation = this.getCurrentConversation();

    if (!conversation) {
      return;
    }

    const updatedConversation: Conversation = {
      ...conversation,
      messages: [
        ...conversation.messages,
        message,
      ],
    };

    this.conversationSubject.next(updatedConversation);
  }

}
