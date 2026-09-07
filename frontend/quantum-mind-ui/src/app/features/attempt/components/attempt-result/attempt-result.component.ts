import {
  ChangeDetectionStrategy,
  Component,
  input,
  OnInit,
  output,
} from '@angular/core';
import { Attempt } from '../../interfaces/attempt.interface';


@Component({
  selector: 'app-attempt-result',
  standalone: false,
  templateUrl: './attempt-result.component.html',
  styleUrl: './attempt-result.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptResultComponent implements OnInit {
  readonly attempt = input.required<Attempt>();

  readonly continue = output<void>();

  readonly retake = output<void>();
  readonly backToExplore = output<void>();
  
  ngOnInit(): void {
    
  }
}