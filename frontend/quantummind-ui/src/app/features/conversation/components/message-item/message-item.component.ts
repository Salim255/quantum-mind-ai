import { Component, Input, SimpleChanges } from "@angular/core";
import { MessageSchema } from "../../model/conversation.model";
import { FinalAnswer } from "../../services/conversation-http.service";

@Component({
  selector: "app-message-item",
  templateUrl: "./message-item.component.html",
  styleUrl: "./message-item.component.scss",
  standalone: false
})

export class MessageItemComponent {

  @Input() message: FinalAnswer | undefined;

  ngOnChanges(changes: SimpleChanges): void {
    if(changes) {
      console.log(this.message);
    }
  }
}
