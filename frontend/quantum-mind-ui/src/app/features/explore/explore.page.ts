import {
  Component,
  OnDestroy,
  OnInit,
  signal,
} from '@angular/core';
import { Subscription } from 'rxjs';

import { ExploreService } from './services/explore.service';
import { ExploreTopicDTO } from './interfaces/explore.dtos';


@Component({
  selector: 'app-explore-page',
  templateUrl: './explore.page.html',
  styleUrls: ['./explore.page.scss'],
  standalone: false,
})
export class ExplorePage implements OnInit, OnDestroy {

  private topicsSubscription?: Subscription;

  readonly topics = signal<ExploreTopicDTO[]>([]);

  constructor(
    private readonly exploreService: ExploreService,
  ) {}

  ngOnInit(): void {
    this.subscribeToTopics();
    this.exploreService.fetchTopics();
  }

  private subscribeToTopics(): void {
    this.topicsSubscription = this.exploreService
      .getTopics$
      .subscribe(topics => {
        this.topics.set(topics);
      });
  }

  ngOnDestroy(): void {
    this.topicsSubscription?.unsubscribe();
  }
}