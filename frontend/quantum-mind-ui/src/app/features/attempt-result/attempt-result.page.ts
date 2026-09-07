import {
  ChangeDetectionStrategy,
  Component,
  input,
  output,
} from '@angular/core';
import { Attempt } from '../attempt/interfaces/attempt.interface';


@Component({
  selector: 'app-attempt-result',
  standalone: false,
  templateUrl: './attempt-result.page.html',
  styleUrl: './attempt-result.page.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptResultPage {
  readonly attempt = input.required<Attempt>();

  readonly continue = output<void>();
}