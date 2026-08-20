import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';


@Component({
  selector: 'app-practice-path-card',
  standalone: false,
  templateUrl: './practice-path-card.component.html',
  styleUrl: './practice-path-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticePathCardComponent {

  readonly icon = input.required<string>();

  readonly title = input.required<string>();

  readonly description = input.required<string>();

  readonly route = input.required<string>();
}