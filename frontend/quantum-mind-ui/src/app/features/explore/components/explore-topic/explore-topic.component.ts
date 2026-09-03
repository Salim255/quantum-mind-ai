import {
  ChangeDetectionStrategy,
  Component,
  input,
  OnInit,
} from '@angular/core';
import { Router } from '@angular/router';

import { AttemptService } from '../../../attempt/services/attempt.service';
import { ExploreQuizDTO } from '../../interfaces/explore.dtos';


@Component({
  selector: 'app-explore-topic',
  standalone: false,
  templateUrl: './explore-topic.component.html',
  styleUrl: './explore-topic.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExploreTopicComponent implements OnInit {

  readonly exploreTopic = input.required<ExploreTopicDTO>();


  readonly index =
    input.required<number>();


  constructor(
    private readonly router: Router,
    private readonly attemptService: AttemptService,
  ) {}



  ngOnInit(): void {
    console.log(this.exploreTopic())  
  }

  get actionLabel(): string {

    const latestAttempt =
      this.exploreTopic().latestAttempt;


    if (!latestAttempt) {
      return 'Take the quiz';
    }

    if (latestAttempt.is_completed) {
      return 'Resume quiz';
    }


    return 'Retake quiz';
  }


  openAttempt(): void {

    const latestAttempt = this.exploreTopic().latestAttempt;

    if (
      latestAttempt &&
      !latestAttempt.is_completed
    ) {

      this.navigateToAttempt(
        latestAttempt.id,
      );

      return;
    }


    this.createAttempt();
  }


  private createAttempt(): void {

    const topicId = this.exploreTopic().topic.id;


    this.attemptService
      .createAttempt(topicId)
      .subscribe({
        next:response => {

          this.navigateToAttempt(
            response.data.attempt.id,
          );

        },
      });
  }


  private navigateToAttempt(
    attemptId: string,
  ): void {

    this.router.navigate([
      'attempt',
      attemptId,
    ]);
  }

}