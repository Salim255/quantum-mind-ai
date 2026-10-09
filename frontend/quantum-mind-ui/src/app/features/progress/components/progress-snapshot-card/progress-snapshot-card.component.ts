import { Component, input } from '@angular/core';

@Component({
  selector: 'app-progress-snapshot-card',
  standalone: false,
  templateUrl: './progress-snapshot-card.component.html',
  styleUrl: './progress-snapshot-card.component.scss',
})
export class ProgressSnapshotCardComponent {
  readonly label = input.required<string>();
  readonly value = input.required<string | number>();
  readonly description = input.required<string>();
  readonly icon = input.required<string>();
  readonly featured = input(false);
}
