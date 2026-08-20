import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-practice-overview-header',
  standalone: false,
  templateUrl: './practice-overview-header.component.html',
  styleUrl: './practice-overview-header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticeOverviewHeaderComponent {}