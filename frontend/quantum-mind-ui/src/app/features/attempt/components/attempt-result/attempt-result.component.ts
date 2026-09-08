import {
  ChangeDetectionStrategy,
  Component,
  input,
  OnDestroy,
  OnInit,
  output,
  signal,
} from '@angular/core';
import { Attempt, AttemptQuestion } from '../../interfaces/attempt.interface';
import { AttemptService } from '../../services/attempt.service';
import { Subscription } from 'rxjs';
import { Topic } from '../../../explore/models/topic.model';
import { Router } from '@angular/router';
import { AttemptResultService } from './services/attempt_result.service';


@Component({
  selector: 'app-attempt-result',
  standalone: false,
  templateUrl: './attempt-result.component.html',
  styleUrl: './attempt-result.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptResultComponent implements OnInit, OnDestroy {
  private currentAttemptSubscription!: Subscription
  readonly attempt = signal<Attempt | null>(null);
  readonly topic = signal<Topic>({} as Topic);
  readonly questions = signal<AttemptQuestion[]>([]);

  readonly continue = output<void>();
    
  constructor(
    private attemptResultService: AttemptResultService,
    private route: Router,
    private attemptService: AttemptService
  ) {}

  ngOnInit(): void {
    this.subscribeToCurrentAttempt();
  }


  private subscribeToCurrentAttempt(): void{
    this.currentAttemptSubscription = this.attemptService.getAttempt$.subscribe(attempt => {
      this.attempt.set(attempt);
      this.topic.set(this.attempt()?.topic!);
      this.questions.set(this.topic()?.questions ?? []);
     
    })
  }

  ngOnDestroy(): void {
    this.currentAttemptSubscription?.unsubscribe();
  }

  retakeQuiz(){
    const attemptId = this.attempt()?.id;
    if(!attemptId) return;
    this.attemptService.retakeQuiz(attemptId).subscribe(
      {
        next: () => {
          this.attemptResultService.dismissResult();
          //this.
        },
        error: () => {
          this.backToExplore();
        }
      }
    );
  }

  backToExplore(): void{
    this.attemptResultService.dismissResult();
    this.route.navigate(['/quizzes/explore'])
  }
}