import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';


@Component({
  selector: 'app-progress-next',
  standalone: false,
  templateUrl: './progress-next.component.html',
  styleUrl: './progress-next.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressNextComponent {}