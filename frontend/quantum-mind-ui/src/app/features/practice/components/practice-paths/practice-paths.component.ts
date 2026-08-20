import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';


@Component({
  selector: 'app-practice-paths',
  standalone: false,
  templateUrl: './practice-paths.component.html',
  styleUrl: './practice-paths.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticePathsComponent {}