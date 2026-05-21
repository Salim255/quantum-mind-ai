import { Component } from "@angular/core";
import { ConversationService } from "../../services/conversation.service";
import { ConversationPayload } from "../../services/conversation-http.service";

@Component({
  selector: "app-message-form",
  templateUrl: "./message-form.component.html",
  styleUrl: "./message-form.component.scss",
  standalone: false
})

export class MessageFormComponent {
  constructor(private conservationService: ConversationService){}
  user_message: string = "";
  ask(){}

  submit( ){
    console.log(this.user_message);
    const payload: ConversationPayload = {user_id: "", conversation_id: "", message: this.user_message}
    this.conservationService.sendMessage(payload).subscribe({
      next: (response) => {
        console.log(response);
      },
      error: (err) => {
        console.log(err);
      }
    });
  }
}
