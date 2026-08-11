import { Component, output} from '@angular/core';

@Component({
  selector: 'app-assistant-launcher',
  templateUrl: './assistant-launcher.component.html',
  styleUrl: './assistant-launcher.component.scss',
  standalone: false
})
export class AssistantLauncherComponent {
  readonly openAssistant = output<void>();

  protected onOpenAssistant(): void {
    this.openAssistant.emit();
  }
}
