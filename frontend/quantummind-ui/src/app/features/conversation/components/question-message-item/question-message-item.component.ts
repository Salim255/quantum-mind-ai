import { Component, Input, OnChanges, SimpleChanges} from "@angular/core";
import { MessageSchema } from "../../model/conversation.model";

@Component({
  selector: "app-question-message-item",
  templateUrl: "./question-message-item.component.html",
  styleUrl: "./question-message-item.component.scss",
  standalone: false
})
export class QuestionMessageItemComponent implements OnChanges {
  @Input() message!: MessageSchema;

  ngOnChanges(changes: SimpleChanges): void {
      if(changes){
        console.log(this.message);
      }
  }
}
