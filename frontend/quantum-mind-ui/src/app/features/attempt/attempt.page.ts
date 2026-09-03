import {
  Component,
  computed,
  OnDestroy,
  OnInit,
  signal,
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';

import { ExploreService } from '../explore/services/explore.service';
import { Topic } from '../explore/models/topic.model';
import { Attempt, AttemptQuestion } from './interfaces/attempt.interface';


@Component({
  selector: 'app-attempt-page',
  templateUrl: './attempt.page.html',
  styleUrls: ['./attempt.page.scss'],
  standalone: false,
})
export class AttemptPage implements OnInit, OnDestroy {

  private routeSubscription?: Subscription;


  /* ============================================================
     ATTEMPT
     ------------------------------------------------------------
     The complete attempt returned by the API.
  ============================================================ */

  readonly attempt = signal<Attempt | null>(null);


  /* ============================================================
     TOPIC
     ------------------------------------------------------------
     The topic belonging to the current attempt.
  ============================================================ */

  readonly topic = signal<Topic>({} as Topic);


  /* ============================================================
     QUESTIONS
     ------------------------------------------------------------
     The questions belonging to the current attempt.
     Only one question is exposed through currentQuestion().
  ============================================================ */

  readonly questions = signal<AttemptQuestion[]>([]);


  /* ============================================================
     CURRENT QUESTION
  ============================================================ */

  readonly currentQuestionIndex = signal(0);

  readonly currentQuestion = computed(() => {

    return (
      this.questions()[this.currentQuestionIndex()]
      ?? ({} as AttemptQuestion)
    );

  });


  /* ============================================================
     PAGINATION
  ============================================================ */

  readonly questionNumber = computed(() => {

    return this.questions().length === 0
      ? 0
      : this.currentQuestionIndex() + 1;

  });


  readonly totalQuestions = computed(() => {

    return this.questions().length;

  });


  readonly hasPrevious = computed(() => {

    return this.currentQuestionIndex() > 0;

  });


  readonly hasNext = computed(() => {

    return (
      this.currentQuestionIndex() <
      this.questions().length - 1
    );

  });


  /* ============================================================
     PROGRESS
  ============================================================ */

  readonly progressPercentage = computed(() => {

    const total = this.totalQuestions();

    if (total === 0) {

      return 0;

    }

    return (
      (this.questionNumber() / total) * 100
    );

  });


  /* ============================================================
     ANSWERS
     ------------------------------------------------------------
     Keep the selected answer for each question.
     This allows the user to go back without losing their choice.
  ============================================================ */

  private readonly selectedAnswers =
    signal<Record<string, string>>({});


  readonly selectedAnswerId = computed(() => {

    const question = this.currentQuestion();

    return this.selectedAnswers()[question.id] ?? null;

  });


  /* ============================================================
     CONSTRUCTOR
  ============================================================ */

  constructor(
    private readonly route: ActivatedRoute,
    private readonly exploreService: ExploreService,
  ) {}


  /* ============================================================
     LIFECYCLE
  ============================================================ */

  ngOnInit(): void {

    this.subscribeToRoute();

  }


  /* ============================================================
     ROUTE
  ============================================================ */

  private subscribeToRoute(): void {

    this.routeSubscription =
      this.route.paramMap.subscribe(params => {

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

     The API returns the attempt together with its topic
     and the topic questions.
  ============================================================ */

  private loadAttempt(slug: string): void {

    /*
     * TODO:
     *
     * this.attemptService
     *   .createAttempt(slug)
     *   .subscribe({
     *
     *     next: attempt => {
     *
     *       this.attempt.set(attempt);
     *
     *       this.topic.set(attempt.topic);
     *
     *       this.questions.set(
     *         attempt.topic.questions
     *       );
     *
     *       this.currentQuestionIndex.set(0);
     *
     *       this.selectedAnswers.set({});
     *
     *     }
     *
     *   });
     */


    /*
     * The service will replace this section.
     *
     * The important mapping is:
     *
     * attempt
     *   └── topic
     *        ├── title
     *        ├── category
     *        └── questions[]
     *
     * The page then exposes only:
     *
     * currentQuestion()
     *
     * rather than rendering the complete question list.
     */

  }


  /* ============================================================
     ANSWER SELECTION
  ============================================================ */

  selectAnswer(answerId: string): void {

    const questionId = this.currentQuestion().id;

    if (!questionId) {

      return;

    }

    this.selectedAnswers.update(answers => ({

      ...answers,

      [questionId]: answerId,

    }));

  }


  /* ============================================================
     PREVIOUS QUESTION
  ============================================================ */

  previousQuestion(): void {

    if (!this.hasPrevious()) {

      return;

    }

    this.currentQuestionIndex.update(
      index => index - 1
    );

  }


  /* ============================================================
     SUBMIT ANSWER
     ------------------------------------------------------------
     The actual answer submission will later be connected
     to AttemptService.
  ============================================================ */

  submitAnswer(): void {

    const question = this.currentQuestion();

    const answerId = this.selectedAnswerId();

    if (!question.id || !answerId) {

      return;

    }


    /*
     * TODO:
     *
     * Send the selected answer to the backend.
     *
     * this.attemptService
     *   .submitAnswer({
     *     attemptId: this.attempt()?.id,
     *     questionId: question.id,
     *     answerId,
     *   })
     *   .subscribe(...)
     */


    if (this.hasNext()) {

      this.goToNextQuestion();

      return;

    }


    this.finishAttempt();

  }


  /* ============================================================
     NEXT QUESTION
  ============================================================ */

  private goToNextQuestion(): void {

    if (!this.hasNext()) {

      return;

    }

    this.currentQuestionIndex.update(
      index => index + 1
    );

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
     * this.attemptService
     *   .finishAttempt(this.attempt()!.id)
     *   .subscribe(...)
     *
     * Then navigate to the result page.
     */

  }


  /* ============================================================
     CLEANUP
  ============================================================ */

  ngOnDestroy(): void {

    this.routeSubscription?.unsubscribe();

  }

}