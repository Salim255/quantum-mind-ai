import { Injectable } from "@angular/core";
import {
  AnswerPayload,
  ConversationHttpService,
  ConversationPayload,
  ConversationResponse
} from "./conversation-http.service";
import { BehaviorSubject, Observable, of, tap } from "rxjs";
import { Conversation } from "../model/conversation.model";
import { QuestionService } from "./question.service";
import { AssistantMessage } from "../../ai-assistant/components/assistant-message/assistant-message.component";
import { AssistantConversation } from "../../ai-assistant/components/assistant-conversation/assistant-conversation.component";

@Injectable({providedIn: "root"})
export class ConversationService {
  private conversationSubject = new BehaviorSubject<Conversation| null>(null);

  constructor(
    private questionService: QuestionService,
    private conversationHttpService: ConversationHttpService,
  ){}


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

  private createAssistantConversation(
    title: string,
  ): AssistantConversation {

    const now = new Date();

    return {
      id: crypto.randomUUID(),
      title,
      createdAt: now,
      updatedAt: now,
    };
  }
  sendStreamMessage(payload: ConversationPayload): void {
    //1 Create user message
    const userMessage = this.createUserMessage(payload);

    //2 Create assistant message
    const assistantMessage = this.createAssistantMessage(payload.conversation_id);

    // 3. Add both messages to the current conversation
    this.appendMessages([
      userMessage,
      assistantMessage,
    ]);

    console.log("We are going to the next")
    this.conversationHttpService
    .sendStreamMessage(payload)
    .subscribe({
      next: (chunk: string) => {
        console.log(chunk, "helo from chunk");
        this.appendMessageContent(assistantMessage.id, chunk);
      },
      error: (err) => {console.log(err)},
      complete: () => {}
    });
  }

  setConversation(conversation: Conversation){
    this.conversationSubject.next(conversation);
  }

  fetChConversation():Observable<Conversation>{
    const conversation = new Conversation('conv-1', []);

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

  private appendMessageContent(
    messageId: string,
    chunk: string
  ): void {

    const conversation =
      this.getCurrentConversation();

    console.log(conversation);
    if (!conversation) {
      return;
    }

    conversation.appendContent(
      messageId,
      chunk
    );

    this.conversationSubject.next(
      conversation
    );
  }

  private appendMessages(
    messages: AssistantMessage[]
  ): void {

    const conversation =
      this.getCurrentConversation();

    if (!conversation) {
      return;
    }

    conversation.appendMessages(messages);

    this.conversationSubject.next(
      conversation
    );
  }

}
