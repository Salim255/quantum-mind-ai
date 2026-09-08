import {
  ChangeDetectionStrategy,
  Component,
  Input,
} from '@angular/core';


@Component({
  selector: 'app-attempt-result-score',
  standalone: false,
  templateUrl: './attempt-result-score.component.html',
  styleUrl: './attempt-result-score.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptResultScoreComponent {
  @Input({ required: true })
  score!: number;
}