import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-progress-insights',
  standalone: false,
  templateUrl: './progress-insights.component.html',
  styleUrl: './progress-insights.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressInsightsComponent {}