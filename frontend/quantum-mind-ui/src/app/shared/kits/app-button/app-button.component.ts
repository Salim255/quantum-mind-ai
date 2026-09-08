import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';

type ButtonVariant =
  | 'primary'
  | 'secondary'
  | 'ghost'
  | 'danger';

type ButtonSize =
  | 'small'
  | 'medium'
  | 'large';

type ButtonType =
  | 'button'
  | 'submit'
  | 'reset';

@Component({
  selector: 'app-button',
  standalone: false,
  templateUrl: './app-button.component.html',
  styleUrl: './app-button.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppButtonComponent {
  /**
   * Text displayed inside the button.
   *
   * Optional for icon-only buttons.
   */
  @Input() label?: string;

  /**
   * Visual hierarchy of the action.
   *
   * primary   → main action
   * secondary → important alternative action
   * ghost     → subtle/contextual action
   * danger    → destructive action
   */
  @Input() variant: ButtonVariant = 'primary';

  /**
   * Controls the size of the button.
   */
  @Input() size: ButtonSize = 'medium';

  /**
   * Icon displayed before the label.
   *
   * Example:
   * icon="lucide:sparkles"
   */
  @Input() icon?: string;

  /**
   * Icon displayed after the label.
   */
  @Input() iconAfter?: string;

  /**
   * Whether this is an icon-only button.
   */
  @Input() iconOnly = false;

  /**
   * Native HTML button type.
   */
  @Input() type: ButtonType = 'button';

  /**
   * Prevents interaction with the button.
   */
  @Input() disabled = false;

  /**
   * Displays a loading state and prevents
   * additional interactions.
   */
  @Input() loading = false;

  /**
   * Makes the button take the full available width.
   */
  @Input() fullWidth = false;

  /**
   * Accessible label for icon-only buttons.
   */
  @Input() ariaLabel?: string;

  /**
   * Emits the native mouse event when activated.
   */
  @Output() readonly clicked = new EventEmitter<MouseEvent>();

  /**
   * Handles button activation.
   */
  onClick(event: MouseEvent): void {
    if (this.disabled || this.loading) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    this.clicked.emit(event);
  }
}