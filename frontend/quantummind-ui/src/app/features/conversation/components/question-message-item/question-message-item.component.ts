import { Component, Input, OnChanges, OnDestroy, OnInit, signal, SimpleChanges} from "@angular/core";
import { MessageSchema } from "../../model/conversation.model";
import { Subscription } from "rxjs";
import { ConversationService } from "../../services/conversation.service";
import { MessageService } from "../../services/message.service";
import { AnswerPayload } from "../../services/conversation-http.service";

@Component({
  selector: "app-question-message-item",
  templateUrl: "./question-message-item.component.html",
  styleUrl: "./question-message-item.component.scss",
  standalone: false
})
export class QuestionMessageItemComponent implements OnInit, OnDestroy {
  private messageSubscription!: Subscription;
  message = signal< AnswerPayload | null> (null);

  constructor(private messageService: MessageService){}

  ngOnInit(): void {
    this.subscribeToConversation();
  }

  subscribeToConversation(){
    this.messageSubscription = this.messageService.getMessage$.subscribe((message) => {
      this.message.set(message);
    })
  }

  ngOnDestroy(): void {
    this.messageSubscription?.unsubscribe()
  }
}
