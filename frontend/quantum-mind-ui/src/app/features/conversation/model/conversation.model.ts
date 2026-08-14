import {
  AssistantMessage,
} from "../../ai-assistant/components/assistant-message/assistant-message.component";


export class Conversation {

  private readonly conversationId: string;

  private title: string;

  private readonly createdAt: Date;

  private updatedAt: Date;

  private messages: AssistantMessage[];

  // messageId → index in messages array
  private readonly messagesMap:
    Map<string, number> = new Map();


  constructor(
    conversationId: string,
    title: string,
    createdAt: Date = new Date(),
    updatedAt: Date = createdAt,
    messages: AssistantMessage[] = [],
  ) {

    this.conversationId = conversationId;

    this.title = title;

    this.createdAt = createdAt;

    this.updatedAt = updatedAt;

    this.messages = messages;

    this.buildMessagesMap();
  }


  appendMessage(
    message: AssistantMessage,
  ): void {

    const existingIndex =
      this.messagesMap.get(message.id);


    // Update existing message
    if (existingIndex !== undefined) {

      this.messages[existingIndex] = message;

      this.updatedAt = new Date();

      return;
    }


    // Add new message
    this.messages.push(message);


    // Store new index
    this.messagesMap.set(
      message.id,
      this.messages.length - 1,
    );


    this.updatedAt = new Date();
  }


  appendMessages(
    messages: AssistantMessage[],
  ): void {

    messages.forEach(message =>
      this.appendMessage(message),
    );
  }


  appendContent(
    messageId: string,
    chunk: string,
  ): void {

    const existingIndex =
      this.messagesMap.get(messageId);


    if (existingIndex === undefined) {
      return;
    }


    const message =
      this.messages[existingIndex];


    message.content += chunk;


    this.updatedAt = new Date();
  }


  private buildMessagesMap(): void {

    this.messages.forEach(
      (message, index) => {

        this.messagesMap.set(
          message.id,
          index,
        );

      },
    );
  }


  getConversationId(): string {
    return this.conversationId;
  }


  getTitle(): string {
    return this.title;
  }


  getCreatedAt(): Date {
    return this.createdAt;
  }


  getUpdatedAt(): Date {
    return this.updatedAt;
  }


  getMessages(): AssistantMessage[] {
    return [...this.messages];
  }


  toJSON() {
    return {
      id: this.conversationId,
      title: this.title,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      messages: [...this.messages],
    };
  }

}
