export interface MessageSchema {
  question: string;
  response: any;
}
export class Conversation {
  private user_id: string;
  private conversation_id: string;
  private messages: MessageSchema []

  constructor(
    conversation_id: string,
    user_id: string,
    messages: MessageSchema []
  ){
    this.user_id = user_id;
    this.conversation_id = conversation_id;
    this.messages = messages
  }

  appendMessage(message: MessageSchema){

  }

  getUerId(): string{
    return this.user_id;
  }
  getMessages(): MessageSchema[]{
    return this.messages;
  }

  getConversationId(): string{
    return this.conversation_id;
  }

}
