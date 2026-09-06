import {
  ChangeDetectionStrategy,
  Component,
  input,
  output,
} from '@angular/core';
import { AttemptAnswer } from '../../interfaces/attempt.interface';

@Component({
  selector: 'app-answer-item',
  standalone: false,
  templateUrl: './answer-item.component.html',
  styleUrl: './answer-item.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AnswerItemComponent {

  /**
   * Answer represented by this option.
   */
  readonly answer = input.required<AttemptAnswer>();

  /**
   * Zero-based position of the answer in the question.
   *
   * The template converts this to a one-based,
   * two-digit display:
   *
   * 0 -> 01
   * 1 -> 02
   * 2 -> 03
   */
  readonly index = input.required<number>();

  /**
   * Whether this answer is currently selected.
   */
  readonly selected = input<boolean>(false);

  /**
   * Emits the answer identifier when the user selects
   * this answer.
   */
  readonly answerSelected = output<AttemptAnswer['id']>();


  /**
   * Keeps the template expressive and avoids repeating
   * the selection comparison.
   */
  protected readonly isSelected = () => this.selected();


  /**
   * Notify the parent that this answer was selected.
   */
  protected select(): void {
    this.answerSelected.emit(this.answer().id);
  }
}