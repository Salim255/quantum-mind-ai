import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';

import { RouterLink } from '@angular/router';

type ProgressInsightVariant =
  | 'strength'
  | 'focus';

@Component({
  selector: 'app-progress-insight-card',
  standalone: false,
  templateUrl: './progress-insight-card.component.html',
  styleUrl: './progress-insight-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressInsightCardComponent {

  readonly variant =
    input<ProgressInsightVariant>('strength');

  readonly label =
    input.required<string>();

  readonly title =
    input.required<string>();

  readonly description =
    input.required<string>();

  readonly actionLabel =
    input<string>('Review topic');

  readonly actionLink =
    input.required<string>();

  readonly icon =
    input.required<string>();
}