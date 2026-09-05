import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';
import { Topic } from '../../../explore/models/topic.model';

@Component({
  selector: 'app-attempt-header',
  standalone: false,
  templateUrl: './attempt-header.component.html',
  styleUrl: './attempt-header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptHeaderComponent {

  /**
   * Topic currently being attempted.
   */
  readonly topic = input.required<Topic>();

  /**
   * Current question number.
   */
  readonly questionNumber = input.required<number>();

  /**
   * Total number of questions in the attempt.
   */
  readonly totalQuestions = input.required<number>();

  /**
   * Calculates the current progress percentage.
   *
   * Example:
   * question 5 / 15 → 33.33%
   */
  protected readonly progressPercentage = () => {
    const total = this.totalQuestions();

    if (!total) {
      return 0;
    }

    return (this.questionNumber() / total) * 100;
  };
}