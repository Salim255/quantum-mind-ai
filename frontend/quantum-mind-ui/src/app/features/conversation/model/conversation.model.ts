import { AssistantMessage } from "../../ai-assistant/components/assistant-message/assistant-message.component";

export class Conversation {

  private conversation_id: string;

  private messages: AssistantMessage[];

  // messageId → index in messages array
  private messagesMap: Map<string, number> = new Map();


  constructor(
    conversation_id: string,
    messages: AssistantMessage[] = [],
  ) {

    this.conversation_id = conversation_id;

    this.messages = messages;

    this.buildMessagesMap();
  }


  appendMessage(message: AssistantMessage): void {

    const existingIndex =
      this.messagesMap.get(message.id);


    // Update existing message
    if (existingIndex !== undefined) {

      this.messages[existingIndex] = message;

      return;
    }


    // Add new message
    this.messages.push(message);


    // Store new index
    this.messagesMap.set(
      message.id,
      this.messages.length - 1,
    );
  }


  appendMessages(messages: AssistantMessage[]): void {

    messages.forEach(message => {
      this.appendMessage(message);
    });
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
  }


  private buildMessagesMap(): void {

    this.messages.forEach((message, index) => {

      this.messagesMap.set(
        message.id,
        index,
      );

    });
  }


  getMessages(): AssistantMessage[] {
    return [...this.messages];
  }


  getConversationId(): string {
    return this.conversation_id;
  }


  toJSON() {
    return {
      conversation_id: this.conversation_id,
      messages: [...this.messages],
    };
  }
}
