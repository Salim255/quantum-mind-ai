import {
  ChangeDetectionStrategy,
  Component,
  input,
  output,
} from '@angular/core';

@Component({
  selector: 'app-attempt-footer',
  standalone: false,
  templateUrl: './attempt-footer.component.html',
  styleUrl: './attempt-footer.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptFooterComponent {

  /**
   * Current one-based question number.
   */
  readonly questionNumber = input.required<number>();

  /**
   * Total number of questions in the attempt.
   */
  readonly totalQuestions = input.required<number>();

  /**
   * Whether the user can navigate to a previous question.
   */
  readonly hasPrevious = input<boolean>(false);

  /**
   * Whether another question exists after the current one.
   */
  readonly hasNext = input<boolean>(false);

  /**
   * Currently selected answer identifier.
   */
  readonly selectedAnswerId = input<string | null>(null);


  /**
   * Emitted when the user requests the previous question.
   */
  readonly previous = output<void>();

  /**
   * Emitted when the user submits the current answer.
   */
  readonly continue = output<void>();


  protected previousQuestion(): void {
    this.previous.emit();
  }


  protected submitAnswer(): void {
    this.continue.emit();
  }
}