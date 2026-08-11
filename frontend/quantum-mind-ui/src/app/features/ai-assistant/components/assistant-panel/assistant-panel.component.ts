import {
  ChangeDetectionStrategy,
  Component,
  output,
} from '@angular/core';

@Component({
  selector: 'app-assistant-panel',
  templateUrl: './assistant-panel.component.html',
  styleUrl: './assistant-panel.component.scss',
  standalone: false
})
export class AssistantPanelComponent {
  readonly close = output<void>();

  protected onClose(): void {
    this.close.emit();
  }
}
