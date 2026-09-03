import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { Topic } from '../../models/topic.model';
import { AttemptService } from '../../../attempt/services/attempt.service';


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

  constructor(private attemptService: AttemptService ){}
  
  fetchAttempt(){
    this.attemptService.
  }

}