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

  readonly retake = output<void>();
  readonly backToExplore = output<void>();

  constructor(private attemptService: AttemptService) {}

  ngOnInit(): void {
    this.subscribeToCurrentAttempt();
  }


  private subscribeToCurrentAttempt(): void{
    this.currentAttemptSubscription = this.attemptService.getAttempt$.subscribe(attempt => {

      console.log(attempt, "hello from attempt");
      this.attempt.set(attempt);
      this.topic.set(this.attempt()?.topic!);
      this.questions.set(this.topic()?.questions ?? []);
     
    })
  }

  ngOnDestroy(): void {
    this.currentAttemptSubscription?.unsubscribe();
  }
}