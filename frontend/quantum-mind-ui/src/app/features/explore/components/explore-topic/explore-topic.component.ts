import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { Topic } from '../../models/topic.model';


@Component({
  selector: 'app-explore-topic',
  standalone: false,
  templateUrl: './explore-topic.component.html',
  styleUrl: './explore-topic.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExploreTopicComponent {

  readonly topic = input.required<Topic>();
  readonly index = input.required<number>();

}