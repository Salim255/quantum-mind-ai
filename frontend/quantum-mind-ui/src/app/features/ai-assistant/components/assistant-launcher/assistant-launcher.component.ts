import { Component, output} from '@angular/core';
import { AIAssistantService } from '../../service/ai-assistant.service';

@Component({
  selector: 'app-assistant-launcher',
  templateUrl: './assistant-launcher.component.html',
  styleUrl: './assistant-launcher.component.scss',
  standalone: false
})
export class AssistantLauncherComponent {
  readonly openAssistant = output<void>();

  constructor(private aiAssistantService: AIAssistantService){}

  protected onOpenAssistant(): void {
    this.aiAssistantService.showAssistant();
  }

}
