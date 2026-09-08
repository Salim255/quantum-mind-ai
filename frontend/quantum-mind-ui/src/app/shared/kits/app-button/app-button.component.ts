import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';

@Component({
  selector: 'app-button',
  standalone: true,
  templateUrl: './app-button.component.html',
  styleUrl: './app-button.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppButtonComponent {
  /**
   * Text displayed inside the button.
   */
  @Input() label = '';

  /**
   * Native button type.
   */
  @Input() type: 'button' | 'submit' | 'reset' = 'button';

  /**
   * Prevents interaction with the button.
   */
  @Input() disabled = false;

  /**
   * Indicates that an action is currently in progress.
   */
  @Input() loading = false;

  /**
   * Emits when the button is clicked.
   */
  @Output() readonly clicked = new EventEmitter<void>();

  /**
   * Handles button interaction.
   *
   * A loading button must not emit another click event.
   */
  onClick(): void {
    if (this.disabled || this.loading) {
      return;
    }

    this.clicked.emit();
  }
}