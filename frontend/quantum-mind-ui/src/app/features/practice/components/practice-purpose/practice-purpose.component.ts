import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';


@Component({
  selector: 'app-practice-purpose',
  standalone: true,
  templateUrl: './practice-purpose.component.html',
  styleUrl: './practice-purpose.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticePurposeComponent {}