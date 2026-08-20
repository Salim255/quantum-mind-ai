import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-practice-home-header',
  standalone: false,
  templateUrl: './practice-home-header.component.html',
  styleUrl: './practice-home-header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticeHomeHeaderComponent {}