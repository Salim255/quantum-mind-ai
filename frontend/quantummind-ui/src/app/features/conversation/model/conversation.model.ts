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
    // 1 Check if the message already exist
    const existingIndex = this.messagesMap.get(message.id);

    // 2 update existing message
    if(existingIndex !== undefined) {
      this.messages[existingIndex] = message;
      return;
    }

    // 3 add new message
    this.messages.push(message);

    // 4 Store new index in map
    this.messagesMap.set(message.id, this.messages.length - 1 );
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
