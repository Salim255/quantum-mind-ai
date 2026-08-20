import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-progress-ranking',
  standalone: false,
  templateUrl: './progress-ranking.component.html',
  styleUrl: './progress-ranking.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressRankingComponent {}