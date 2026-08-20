import { Component, input } from '@angular/core';


@Component({
  selector: 'app-practice-overview-progress-card',
  standalone: false,
  templateUrl: './practice-overview-progress-card.component.html',
  styleUrl: './practice-overview-progress-card.component.scss',
})
export class PracticeOverviewProgressCardComponent {

  readonly title = input.required<string>();

  readonly meta = input.required<string>();

  readonly progress = input.required<string>();

  readonly icon = input.required<string>();

  readonly link = input.required<string>();
}