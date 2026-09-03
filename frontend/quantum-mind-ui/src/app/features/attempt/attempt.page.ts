import {
  Component,
  OnDestroy,
  OnInit,
  signal,
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';

import { ExploreService } from '../explore/services/explore.service';
import { Topic } from '../explore/models/topic.model';
import { Attempt } from './interfaces/attempt.interface';


interface AttemptAnswer {
  id: string;
  text: string;
}

interface AttemptQuestion {
  id: string;
  question: string;
  answers: AttemptAnswer[];
}

@Component({
  selector: 'app-attempt-page',
  templateUrl: './attempt.page.html',
  styleUrls: ['./attempt.page.scss'],
  standalone: true,
})
export class AttemptPage implements OnInit, OnDestroy {

  private routeSubscription?: Subscription;


  /*
   * The current quiz attempt.
   */
  readonly attempt = signal<Attempt | null>(null);


  /*
   * Questions belonging to the current attempt.
   *
   * We keep them as the backing collection,
   * but expose only one question through
   * currentQuestion().
   */
  readonly questions = signal<AttemptQuestion[]>([]);


  /*
   * Index of the question currently displayed.
   */
  readonly currentQuestionIndex = signal(0);


  /*
   * Currently selected answer.
   */
  readonly selectedAnswerId = signal<string | null>(null);


  constructor(

    private readonly route: ActivatedRoute,

  ) {}


  ngOnInit(): void {

    this.subscribeToRoute();

  }


  /* ============================================================
     ROUTE
  ============================================================ */

  private subscribeToRoute(): void {

    this.routeSubscription = this.route.paramMap.subscribe(params => {

      const topicSlug = params.get('slug');

      if (!topicSlug) {

        return;

      }

      this.loadAttempt(topicSlug);

    });

  }


  /* ============================================================
     ATTEMPT
     ------------------------------------------------------------
     This will later call AttemptService.
  ============================================================ */

  private loadAttempt(slug: string): void {

    /*
     * TODO:
     *
     * this.attemptService
     *   .createAttempt(slug)
     *   .subscribe(attempt => {
     *
     *     this.attempt.set(attempt);
     *
     *     this.questions.set(
     *       attempt.topic.questions
     *     );
     *
     *   });
     *
     *
     * For now the page structure is ready
     * for the real AttemptService.
     */

  }


  /* ============================================================
     CURRENT QUESTION
  ============================================================ */

  readonly currentQuestion = (): AttemptQuestion | null => {

    return this.questions()[this.currentQuestionIndex()]
      ?? null;

  };


  /* ============================================================
     PROGRESS
  ============================================================ */

  readonly progressPercentage = (): number => {

    const total = this.questions().length;

    if (total === 0) {

      return 0;

    }

    return (
      ((this.currentQuestionIndex() + 1) / total) * 100
    );

  };


  /* ============================================================
     ANSWER SELECTION
  ============================================================ */

  selectAnswer(answerId: string): void {

    this.selectedAnswerId.set(answerId);

  }


  /* ============================================================
     SUBMIT ANSWER
     ------------------------------------------------------------
     The actual answer submission will be connected
     to AttemptService once the endpoint is defined.
  ============================================================ */

  submitAnswer(): void {

    const answerId = this.selectedAnswerId();

    if (!answerId) {

      return;

    }

    /*
     * TODO:
     *
     * Send the selected answer to the backend.
     *
     * this.attemptService
     *   .submitAnswer(...)
     *   .subscribe(...)
     */

    this.goToNextQuestion();

  }


  /* ============================================================
     NEXT QUESTION
  ============================================================ */

  private goToNextQuestion(): void {

    const nextIndex =
      this.currentQuestionIndex() + 1;


    /*
     * Last question.
     */
    if (nextIndex >= this.questions().length) {

      this.finishAttempt();

      return;

    }


    this.currentQuestionIndex.set(nextIndex);

    this.selectedAnswerId.set(null);

  }


  /* ============================================================
     FINISH
  ============================================================ */

  private finishAttempt(): void {

    /*
     * TODO:
     *
     * Finish the attempt through AttemptService.
     *
     * We will decide whether to navigate to
     * a result page or display the result here.
     */

  }


  /* ============================================================
     CLEANUP
  ============================================================ */

  ngOnDestroy(): void {

    this.routeSubscription?.unsubscribe();

  }

}