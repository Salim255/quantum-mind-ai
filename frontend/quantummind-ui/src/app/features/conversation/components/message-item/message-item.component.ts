import { Component, Input, SimpleChanges } from "@angular/core";
import { MessageSchema } from "../../model/conversation.model";

@Component({
  selector: "app-message-item",
  templateUrl: "./message-item.component.html",
  styleUrl: "./message-item.component.scss",
  standalone: false
})

export class MessageItemComponent {
  @Input() message!: MessageSchema;

  ngOnChanges(changes: SimpleChanges): void {
    if(changes) {
      console.log(this.message);
    }
  }
}
