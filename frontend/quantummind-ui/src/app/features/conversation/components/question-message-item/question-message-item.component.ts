import { Component, Input, OnChanges, SimpleChanges} from "@angular/core";
import { MessageSchema } from "../../model/conversation.model";
import { Subscription } from "rxjs";

@Component({
  selector: "app-question-message-item",
  templateUrl: "./question-message-item.component.html",
  styleUrl: "./question-message-item.component.scss",
  standalone: false
})
export class QuestionMessageItemComponent implements OnChanges {
  @Input() message!: MessageSchema;

  private conversationSubscription!: Subscription;

  constructor(){}

  ngOnChanges(changes: SimpleChanges): void {
      if(changes){
        console.log(this.message);
      }
  }

  ngOnDestroy(): void {
    this.conversationSubscription?.unsubscribe()
  }
}
