import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';


@Component({
  selector: 'app-practice-overview-metric-card',
  standalone: false,
  templateUrl: './practice-overview-metric-card.component.html',
  styleUrl: './practice-overview-metric-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticeOverviewMetricCardComponent {

  readonly icon = input.required<string>();

  readonly label = input.required<string>();

  readonly value = input.required<string>();

  readonly description = input.required<string>();

  readonly actionLabel = input<string>();

  readonly actionRoute = input<string>();

  readonly context = input<string>();

}