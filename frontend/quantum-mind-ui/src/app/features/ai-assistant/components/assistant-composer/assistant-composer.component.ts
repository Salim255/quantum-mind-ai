import { Component } from "@angular/core";
import { ConversationPayload } from "../../../conversation/services/conversation-http.service";
import { ConversationService } from "../../../conversation/services/conversation.service";
@Component({
  selector: "app-assistant-composer",
  templateUrl: "./assistant-composer.component.html",
  styleUrl: "./assistant-composer.component.scss",
  standalone: false
})
export class AssistantComposerComponent {
  message = "";

  constructor(private conservationService: ConversationService){}

  onSubmit(){
    const payload: ConversationPayload = { conversation_id: "", message: this.message};

    this.conservationService.sendStreamMessage(payload);
  }
}
