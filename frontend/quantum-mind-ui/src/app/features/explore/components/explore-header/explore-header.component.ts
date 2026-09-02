import {
  ChangeDetectionStrategy,
  Component,
} from '@angular/core';

@Component({
  selector: 'app-explore-header',
  standalone: false,
  templateUrl: './explore-header.component.html',
  styleUrl: './explore-header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExploreHeaderComponent {}