import { ChangeDetectionStrategy, Component } from '@angular/core';


@Component({
  selector: 'app-practice-overview-snapshot',
  standalone: false,
  templateUrl: './practice-overview-snapshot.component.html',
  styleUrl: './practice-overview-snapshot.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticeOverviewSnapshotComponent {}