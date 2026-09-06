import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';

import { AttemptQuestion } from '../../interfaces/attempt.interface';

@Component({
  selector: 'app-question',
  standalone: false,
  templateUrl: './question.component.html',
  styleUrl: './question.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class QuestionComponent {

  /**
   * Question currently displayed to the user.
   */
  readonly question = input.required<AttemptQuestion>();

  /**
   * One-based position of the question in the attempt.
   *
   * Example:
   * 1 -> "01"
   * 7 -> "07"
   * 15 -> "15"
   */
  readonly questionNumber = input.required<number>();
}