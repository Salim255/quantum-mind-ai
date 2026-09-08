import {
  ChangeDetectionStrategy,
  Component,
  Input,
} from '@angular/core';

@Component({
  selector: 'app-attempt-result-header',
  standalone: false,
  templateUrl: './attempt-result-header.component.html',
  styleUrl: './attempt-result-header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptResultHeaderComponent {
  @Input({ required: true })
  topicTitle!: string;
}