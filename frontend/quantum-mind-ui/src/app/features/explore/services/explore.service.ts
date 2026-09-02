import { Injectable } from '@angular/core';
import { BehaviorSubject, map, Observable } from 'rxjs';

import { Topic } from '../models/topic.model';
import { ExploreHttpService } from './explore-http.service';
import { ExploreState } from '../interfaces/explore.dtos';



@Injectable({
  providedIn: 'root',
})
export class ExploreService {

  private readonly stateSubject =
    new BehaviorSubject<ExploreState>({
      topics: [],
    });


  private readonly state$ =
    this.stateSubject.asObservable();


  constructor( private readonly exploreService: ExploreHttpService) {}



  fetchTopics(): void {

    this.exploreService
      .getTopics()
      .subscribe( response => {
          this.setTopics(response.data.topics);
        });

  }


  /**
   * Returns the current topics as an observable.
   */
  getTopics$(): Observable<Topic[]> {

    return this.state$.pipe(
      map(state => state.topics),
    );

  }


  /**
   * Updates the topics stored in the Explore state.
   */
  private setTopics(topics: Topic[]): void {

    this.stateSubject.next({
      topics,
    });

  }

}