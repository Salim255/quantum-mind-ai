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

  submit(){
    const payload: ConversationPayload = {user_id: "", conversation_id: "", message: this.user_message}
    this.conservationService.sendStreamMessage(payload);
    this.user_message = "";
  }

  autoResize(textarea: HTMLTextAreaElement): void {
    // Reset height so the browser recalculates scrollHeight
    textarea.style.height = 'auto';

    // If empty, return to the initial one-row height
    if (!textarea.value.trim()) {
      textarea.style.height = '';
      return;
    }

    // Grow to fit content
    textarea.style.height = `${textarea.scrollHeight}px`;
  }
}
