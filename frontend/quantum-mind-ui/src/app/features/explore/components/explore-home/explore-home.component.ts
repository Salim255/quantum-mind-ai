import {
  Component,
  OnDestroy,
  OnInit,
  signal,
} from '@angular/core';
import { ExploreService } from '../../services/explore.service';
import { Subscription } from 'rxjs';
import { ExploreQuizDTO } from '../../interfaces/explore.dtos';


@Component({
  selector: 'app-explore-home',
  templateUrl: './explore-home.component.html',
  styleUrls: ['./explore-home.component.scss'],
  standalone: false,
})
export class ExploreHomeComponent implements OnInit, OnDestroy {

   private topicsSubscription?: Subscription;

  readonly topics = signal<ExploreQuizDTO[]>([]);

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