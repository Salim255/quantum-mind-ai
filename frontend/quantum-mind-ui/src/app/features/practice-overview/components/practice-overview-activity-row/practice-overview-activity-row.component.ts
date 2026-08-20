import { Component, input } from '@angular/core';


@Component({
  selector: 'app-practice-overview-activity-row',
  standalone: false,
  templateUrl: './practice-overview-activity-row.component.html',
  styleUrl: './practice-overview-activity-row.component.scss',
})
export class PracticeOverviewActivityRowComponent {

  readonly topic = input.required<string>();

  readonly meta = input.required<string>();

  readonly score = input.required<string>();

  readonly link = input.required<string>();
}