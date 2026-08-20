import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-practice-home-footer',
  standalone: false,
  templateUrl: './practice-home-footer.component.html',
  styleUrl: './practice-home-footer.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticeHomeFooterComponent {}