import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-progress-activity',
  standalone: false,
  templateUrl: './progress-activity.component.html',
  styleUrl: './progress-activity.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressActivityComponent {}