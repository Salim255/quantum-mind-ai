import { Component, OnDestroy, OnInit, signal } from "@angular/core";
import { Subscription } from "rxjs";
import { ConversationService } from "../../services/conversation.service";
import { Conversation, MessageSchema } from "../../model/conversation.model";

@Component({
  selector: "app-messages",
  templateUrl: "./messages.component.html",
  styleUrls: ["./messages.component.scss"],
  standalone:false
})
export class MessagesComponent implements OnInit, OnDestroy {
  conversationSubscription!: Subscription;
  private conversation: Conversation | null = null;
  messages = signal<MessageSchema[]>([]);

  constructor(private conversationService: ConversationService) {}

  ngOnInit(): void {
    this.conversationService.fetChConversation().subscribe();
    this.subscribeToConversation()
  }

  subscribeToConversation(): void{
    this.conversationSubscription = this.conversationService
    .getConversation.subscribe((conversation: Conversation | null) => {
      this.conversation = conversation;
      this.messages.set(this.conversation?.getMessages()?? []);
      console.log(this.conversation, this.messages());
    })
  }

  ngOnDestroy(): void {
    this.conversationSubscription?.unsubscribe();
  }
}
