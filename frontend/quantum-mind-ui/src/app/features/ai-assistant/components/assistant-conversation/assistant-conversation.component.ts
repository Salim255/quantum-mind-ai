import { Component, signal } from "@angular/core";
import { AssistantMessage } from "../assistant-message/assistant-message.component";
import { ConversationService } from "../../../conversation/services/conversation.service";
import { Subscription } from "rxjs";


export interface AssistantConversation {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}

@Component({
  selector: "app-assistant-conversation",
  templateUrl: "./assistant-conversation.component.html",
  styleUrl: "./assistant-conversation.component.scss",
  standalone: false
})
export class AssistantConversationComponent {

  private conversationSubscription!: Subscription;
  messages = signal<AssistantMessage []>([]);

  constructor( private conversationService: ConversationService){}


  ngOnInit(): void {
    this.subscribeToConversation();
  }

  subscribeToConversation(){
    this.conversationSubscription = this.conversationService
      .getConversation
      .subscribe(conversation => {
        this.messages.set(conversation?.getMessages() ?? []);
      })
  }

  ngOnDestroy(): void {
    this.conversationSubscription?.unsubscribe();
  }
}
