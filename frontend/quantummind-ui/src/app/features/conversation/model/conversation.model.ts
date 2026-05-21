export interface MessageSchema {
  id: string;
  question: string;
  response: any;
}
export class Conversation {
  private userId: string;
  private conversationId: string;
  private messages: MessageSchema []
  private messagesMap: Map<string, number>  = new Map();

  constructor(
    conversation_id: string,
    user_id: string,
    messages: MessageSchema []
  ){
    this.userId = user_id;
    this.conversationId = conversation_id;
    this.messages = messages;

    this.buildMessagesMap();
  }

  appendMessage(message: MessageSchema){

  }

  getUerId(): string{
    return this.userId;
  }

  buildMessagesMap(): void{
    this.messages.forEach((message, index) => {
      this.messagesMap.set(message.id, index);
    });
  }

  getMessages(): MessageSchema[]{
    return this.messages;
  }

  getConversationId(): string{
    return this.conversationId;
  }

}
