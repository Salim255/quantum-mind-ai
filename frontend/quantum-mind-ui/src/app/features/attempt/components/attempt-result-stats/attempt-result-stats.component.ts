import {
  ChangeDetectionStrategy,
  Component,
  Input,
} from '@angular/core';

@Component({
  selector: 'app-attempt-result-stats',
  standalone: false,
  templateUrl: './attempt-result-stats.component.html',
  styleUrl: './attempt-result-stats.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptResultStatsComponent {
  @Input({ required: true })
  correctAnswers!: number;

  @Input({ required: true })
  totalQuestions!: number;

  get incorrectAnswers(): number {
    return this.totalQuestions - this.correctAnswers;
  }
}