import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';


@Component({
  selector: 'app-practice-purpose',
  standalone: false,
  templateUrl: './practice-purpose.component.html',
  styleUrl: './practice-purpose.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticePurposeComponent {}