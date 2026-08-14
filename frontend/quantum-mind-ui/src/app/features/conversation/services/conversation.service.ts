import { Injectable } from "@angular/core";
import { ConversationHttpService, ConversationPayload } from "./conversation-http.service";
import { BehaviorSubject, Observable, of, tap } from "rxjs";
import { Conversation } from "../model/conversation.model";
import { AssistantMessage } from "../../ai-assistant/components/assistant-message/assistant-message.component";

@Injectable({providedIn: "root"})
export class ConversationService {
  private conversationSubject = new BehaviorSubject<Conversation| null>(null);

  constructor(private conversationHttpService: ConversationHttpService){}


  private createUserMessage(message: string): AssistantMessage {

    return {
      id: crypto.randomUUID(),
      conversationId: this.getCurrentConversation()?.getConversationId() ?? "",
      role: "user",
      content: message,
      createdAt: new Date(),
    };
  }


  private createAssistantMessage(): AssistantMessage {

    return {
      id: crypto.randomUUID(),
      conversationId: this.getCurrentConversation()?.getConversationId() ?? "",
      role: "assistant",
      status: 'thinking',
      content: "",
      createdAt: new Date(),
    };
  }


  sendStreamMessage(
    payload: ConversationPayload & { title: string }
  ): void {

    if(!this.getCurrentConversation()){
      this.createAssistantConversation(payload.title);
    }


    //1 Create user message
    const userMessage = this.createUserMessage(payload.message);

    //2 Create assistant message
    const assistantMessage = this.createAssistantMessage();

    // 3. Add both messages to the current conversation
    this.appendMessages([
      userMessage,
      assistantMessage,
    ]);

    this.conversationHttpService
    .sendStreamMessage({
      conversation_id: this.getCurrentConversation()?.getConversationId() ?? "",
      message: payload.message
    })
    .subscribe({
      next: (chunk: string) => {

        this.appendMessageContent(assistantMessage.id, chunk);
      },
      error: (err) => {console.log(err)},
      complete: () => {}
    });
  }

  setConversation(conversation: Conversation){
    this.conversationSubject.next(conversation);
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

  private createAssistantConversation(
      title: string,
    ): void {

    this.setConversation(new Conversation(
      crypto.randomUUID(),
      title,
    ))
  }

}
