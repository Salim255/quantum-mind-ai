import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';
import { ExploreCategory } from '../../interfaces/explore.dtos';


@Component({
  selector: 'app-explore-category',
  standalone: false,

  templateUrl: './explore-category.component.html',
  styleUrl: './explore-category.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExploreCategoryComponent {

  readonly category = input.required<ExploreCategory>();

  protected readonly topics = () => this.category().topics;

}