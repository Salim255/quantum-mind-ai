import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';

@Component({
  selector: 'app-progress-knowledge-card',
  standalone: false,
  templateUrl: './progress-knowledge-card.component.html',
  styleUrl: './progress-knowledge-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressKnowledgeCardComponent {

  readonly title = input.required<string>();

  readonly status = input.required<string>();

  readonly score = input.required<string>();

  readonly icon = input.required<string>();

  readonly progress = input.required<number>();
}