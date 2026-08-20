import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-practice-guidance',
  standalone: false,
  templateUrl: './practice-guidance.component.html',
  styleUrl: './practice-guidance.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticeGuidanceComponent {}