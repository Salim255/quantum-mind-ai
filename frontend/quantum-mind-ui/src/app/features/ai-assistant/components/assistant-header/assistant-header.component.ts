import { Component, output } from "@angular/core";
import { AIAssistantService } from "../../service/ai-assistant.service";

@Component({
  selector: "app-assistant-header",
  templateUrl: "./assistant-header.component.html",
  styleUrl: "./assistant-header.component.scss",
  standalone: false
})
export class AssistantHeaderComponent {

  constructor(private aiAssistantService: AIAssistantService){}

  protected onCloseAssistant(): void {
    this.aiAssistantService.toggleAssistant();
  }
}
