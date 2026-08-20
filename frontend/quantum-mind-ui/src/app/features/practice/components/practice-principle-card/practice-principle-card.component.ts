import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';

@Component({
  selector: 'app-practice-principle-card',
  standalone: false,
  templateUrl: './practice-principle-card.component.html',
  styleUrl: './practice-principle-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticePrincipleCardComponent {

  readonly icon = input.required<string>();

  readonly title = input.required<string>();

  readonly description = input.required<string>();
}