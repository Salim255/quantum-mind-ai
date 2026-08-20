import { ChangeDetectionStrategy, Component } from '@angular/core';


@Component({
  selector: 'app-progress-achievements',
  standalone: false,
  templateUrl: './progress-achievements.component.html',
  styleUrl: './progress-achievements.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressAchievementsComponent {}