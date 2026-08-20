import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-progress-snapshot',
  standalone: false,
  templateUrl: './progress-snapshot.component.html',
  styleUrl: './progress-snapshot.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressSnapshotComponent {}