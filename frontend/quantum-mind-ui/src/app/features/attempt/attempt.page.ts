import {
  Component,
  computed,
  OnDestroy,
  OnInit,
  signal,
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';

import { Topic } from '../explore/models/topic.model';
import { Attempt, AttemptQuestion } from './interfaces/attempt.interface';
import { AttemptService } from './services/attempt.service';
import { AttemptResultComponent } from './components/attempt-result/attempt-result.component';
import { ModalVariant } from '../../shared/kits/modal/modal-config';
import { AttemptResultService } from './components/attempt-result/services/attempt_result.service';


@Component({
  selector: 'app-attempt-page',
  templateUrl: './attempt.page.html',
  styleUrls: ['./attempt.page.scss'],
  standalone: false,
})
export class AttemptPage implements OnInit, OnDestroy {
  private retakeQuizSubscription!: Subscription;
  private currentAttemptSubscription!: Subscription
  private routeSubscription?: Subscription;
  private attemptResultSubscription?: Subscription;


  readonly attempt = signal<Attempt | null>(null);


  readonly topic = signal<Topic>({} as Topic);



  readonly questions = signal<AttemptQuestion[]>([]);


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

  showResult = signal<boolean>(false);

  protected readonly attemptResultModalConfig = {

    component: AttemptResultComponent,

    variant: 'dialog' as ModalVariant,

    size: 'full' as const,

    title: 'Assessment result',

    showClose: false,

    closeOnBackdrop: false,

    closeOnEscape: false,

    onClose: () => {
      this.closeResult();
    },

  };

  /* ============================================================
  CONSTRUCTOR
  ============================================================ */

  constructor(
    private readonly route: Router,
    private attempt_result_service: AttemptResultService,
    private attemptService: AttemptService,
  ) {}


  /* ============================================================
  LIFECYCLE
  ============================================================ */

  ngOnInit(): void {
    this.subscribeToCurrentAttempt();
    this.subscribeToAttemptResult();
    this.subscribeToRetakeQuiz();
    if(!this.attempt()) {
      this.route.navigate(["/quizzes/explore"]) 
    }
  }



  private subscribeToRetakeQuiz(): void{
    this.retakeQuizSubscription = this.attemptService.retake$.subscribe(isRetake => {
      if (isRetake) {
        this.currentQuestionIndex.set(0);
        this.selectedAnswers.set({})
      }
    })
  }
  private subscribeToAttemptResult(): void{
    this.attemptResultSubscription = this.attempt_result_service
    .getShowResult$
    .subscribe(status => {
      this.showResult.set(status && (this.attempt()?.is_completed === true))
    })
  }

  private subscribeToCurrentAttempt(): void{
    this.currentAttemptSubscription = this.attemptService
    .getAttempt$
    .subscribe(attempt => {

      this.attempt.set(attempt);
      this.questions.set(this.attempt()?.topic?.questions ?? []);
      this.topic.set(this.attempt()?.topic!);
    })
  }


  closeResult(){

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


  // ============================================================
  //  SUBMIT ANSWER
  //  ------------------------------------------------------------
  //  The actual answer submission will later be connected
  //  to AttemptService.
  // ============================================================

  submitAnswer(): void {

    const question = this.currentQuestion();

    const answerId = this.selectedAnswerId();

    if (!question.id || !answerId ) {
      return;
    }

    // Send the selected answer to the backend.
    //questionId: question.id,
    this.attemptService
      .submitAnswer(
        answerId,
      )
      .subscribe({
        next: () => {
          if (this.hasNext()) {

            this.goToNextQuestion();
            this.attempt_result_service.showResult();
            
            return;
          }
          this.finishAttempt();
        },
        error: () => {}
      })
  }


  // ============================================================
  // NEXT QUESTION
  // ============================================================

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

  
    this.attemptService
       .finishAttempt()
       .subscribe(
        {
          next: () => {
            this.showResult.set(true);
          },
          error: () => {}
        }
       )
   

  }


  /* ============================================================
  CLEANUP
  ============================================================ */

  ngOnDestroy(): void {
    this.retakeQuizSubscription?.unsubscribe();
    this.attemptResultSubscription?.unsubscribe();
    this.routeSubscription?.unsubscribe();
    this.currentAttemptSubscription.unsubscribe();
  }

}