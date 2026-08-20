import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-progress-header',
  standalone: false,
  templateUrl: './progress-header.component.html',
  styleUrl: './progress-header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressHeaderComponent {}