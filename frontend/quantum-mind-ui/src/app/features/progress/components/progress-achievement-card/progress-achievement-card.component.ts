import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';

type ProgressAchievementVariant =
  | 'complete'
  | 'locked';

@Component({
  selector: 'app-progress-achievement-card',
  standalone: false,
  templateUrl: './progress-achievement-card.component.html',
  styleUrl: './progress-achievement-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressAchievementCardComponent {

  readonly variant =
    input<ProgressAchievementVariant>('complete');

  readonly title =
    input.required<string>();

  readonly description =
    input.required<string>();

  readonly icon =
    input.required<string>();
}