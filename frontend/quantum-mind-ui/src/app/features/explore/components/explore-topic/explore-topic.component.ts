import {
  ChangeDetectionStrategy,
  Component,
  input,
} from '@angular/core';
import { Router } from '@angular/router';

import { AttemptService } from '../../../attempt/services/attempt.service';
import { ExploreTopicDTO } from '../../interfaces/explore.dtos';


@Component({
  selector: 'app-explore-topic',
  standalone: false,
  templateUrl: './explore-topic.component.html',
  styleUrl: './explore-topic.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExploreTopicComponent {

  /*
   * ==========================================================
   * INPUTS
   * ==========================================================
   *
   * ExploreTopicDTO contains:
   *
   *   - the topic
   *   - the current user's latest attempt
   *
   * The component therefore has everything it needs to
   * determine whether the user should start, resume, or
   * retake the quiz.
   */
  readonly exploreTopic =
    input.required<ExploreTopicDTO>();


  readonly index =
    input.required<number>();


  constructor(
    private readonly router: Router,
    private readonly attemptService: AttemptService,
  ) {}


  /*
   * ==========================================================
   * ACTION LABEL
   * ==========================================================
   *
   * Provides the user-facing action for the current topic.
   *
   * We deliberately don't expose backend terminology such as
   * "in_progress" or "completed" to the user.
   */
  get actionLabel(): string {

    const latestAttempt =
      this.exploreTopic().latestAttempt;


    /*
     * No previous attempt.
     */
    if (!latestAttempt) {
      return 'Take the quiz';
    }


    /*
     * Existing unfinished attempt.
     */
    if (latestAttempt.is_completed) {
      return 'Resume quiz';
    }


    /*
     * Existing completed attempt.
     */
    return 'Retake quiz';
  }


  /*
   * ==========================================================
   * OPEN ATTEMPT
   * ==========================================================
   *
   * Determines what should happen when the user selects
   * this topic.
   *
   * Existing in-progress attempt:
   *     → resume it.
   *
   * No attempt:
   *     → create a new one.
   *
   * Completed attempt:
   *     → create a new one.
   */
  openAttempt(): void {

    const latestAttempt =
      this.exploreTopic().latestAttempt;


    /*
     * ========================================================
     * RESUME
     * ========================================================
     *
     * The user already has an unfinished attempt.
     *
     * We don't create another attempt.
     */
    if (
      latestAttempt &&
      !latestAttempt.is_completed
    ) {

      this.navigateToAttempt(
        latestAttempt.id,
      );

      return;
    }


    /*
     * ========================================================
     * START / RETAKE
     * ========================================================
     *
     * Either:
     *
     *   - the user has never attempted this topic
     *   - the previous attempt is completed
     *
     * In both cases we create a new attempt.
     */
    this.createAttempt();
  }


  /*
   * ==========================================================
   * CREATE ATTEMPT
   * ==========================================================
   *
   * Creates a new attempt for the current topic.
   */
  private createAttempt(): void {

    const topicId =
      this.exploreTopic().topic.id;


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


  /*
   * ==========================================================
   * NAVIGATE TO ATTEMPT
   * ==========================================================
   */
  private navigateToAttempt(
    attemptId: string,
  ): void {

    this.router.navigate([
      'attempt',
      attemptId,
    ]);
  }

}