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
  standalone: false,
})
export class AttemptPage implements OnInit, OnDestroy {

  private routeSubscription?: Subscription;

  readonly topic = signal<Topic | null>(null);

  readonly questions = signal<AttemptQuestion[]>([]);

  readonly currentQuestionIndex = signal(0);

  readonly selectedAnswerId = signal<string | null>(null);

  constructor(
    private readonly route: ActivatedRoute,
    private readonly exploreService: ExploreService,
  ) {}

  ngOnInit(): void {
    this.subscribeToRoute();
  }

  private subscribeToRoute(): void {
    this.routeSubscription = this.route.paramMap.subscribe(params => {

      const topicSlug = params.get('slug');

      if (!topicSlug) {
        return;
      }

      this.loadTopic(topicSlug);
    });
  }

  private loadTopic(slug: string): void {

    const topic = this.exploreService
      .getTopicBySlug(slug);

    if (!topic) {
      return;
    }

    this.topic.set(topic);

    /*
     * Questions will be loaded here once the
     * attempt API/service is connected.
     */
    this.questions.set([]);
  }

  readonly currentQuestion = () => {
    return this.questions()[this.currentQuestionIndex()];
  };

  readonly progressPercentage = () => {

    const total = this.questions().length;

    if (total === 0) {
      return 0;
    }

    return (
      ((this.currentQuestionIndex() + 1) / total) * 100
    );
  };

  selectAnswer(answerId: string): void {
    this.selectedAnswerId.set(answerId);
  }

  submitAnswer(): void {

    const answerId = this.selectedAnswerId();

    if (!answerId) {
      return;
    }

    /*
     * Answer submission/evaluation will be connected
     * once the attempt service is implemented.
     */

    this.goToNextQuestion();
  }

  private goToNextQuestion(): void {

    const nextIndex =
      this.currentQuestionIndex() + 1;

    if (nextIndex >= this.questions().length) {
      return;
    }

    this.currentQuestionIndex.set(nextIndex);

    this.selectedAnswerId.set(null);
  }

  ngOnDestroy(): void {
    this.routeSubscription?.unsubscribe();
  }
}