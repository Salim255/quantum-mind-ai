import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-progress-knowledge',
  standalone: false,
  templateUrl: './progress-knowledge.component.html',
  styleUrl: './progress-knowledge.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProgressKnowledgeComponent {}