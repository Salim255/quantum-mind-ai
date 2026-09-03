import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  map,
  Observable,
} from 'rxjs';

import { Topic } from '../models/topic.model';
import { ExploreHttpService } from './explore-http.service';
import { ExploreState, ExploreTopicDTO } from '../interfaces/explore.dtos';



@Injectable({
  providedIn: 'root',
})
export class ExploreService {

  /*
   * ==========================================================
   * STATE
   * ==========================================================
   *
   * The Explore page only needs one piece of state:
   *
   *   topics
   *
   * The API remains the source of truth.
   *
   * We initialize the state with an empty array because
   * topics have not been fetched yet.
   */
  private readonly stateSubject =
    new BehaviorSubject<ExploreState>({
      topics: [],
    });


  /*
   * Expose the state as a read-only observable.
   *
   * Components can observe the state but cannot modify it
   * directly.
   */
  private readonly state$ =
    this.stateSubject.asObservable();


  constructor(
    private readonly exploreHttpService: ExploreHttpService,
  ) {}


  /*
   * ==========================================================
   * FETCH TOPICS
   * ==========================================================
   *
   * Retrieves the topics from the API through the HTTP service
   * and stores them in the Explore state.
   */
  fetchTopics(): void {

    this.exploreHttpService
      .getTopics()
      .subscribe({
        next: response => {

          this.setTopics(
            response.data.topics,
          );

        },
      });
  }


  /*
   * ==========================================================
   * GET TOPICS
   * ==========================================================
   *
   * Returns the topics currently stored in the Explore state.
   *
   * The component receives the actual Topic objects returned
   * by the API, including their:
   *
   * - id
   * - title
   * - slug
   * - category
   * - description
   * - display_order
   * - questions
   *
   * Nothing is reformatted or duplicated here.
   */
  get getTopics$(): Observable<ExploreTopicDTO[]> {

    return this.state$.pipe(
      map(state => state.topics),
    );
  }


  /*
   * ==========================================================
   * SET TOPICS
   * ==========================================================
   *
   * Updates the Explore state.
   *
   * Kept private so that only this service controls
   * state mutation.
   */
  private setTopics(
    topics: ExploreTopicDTO[],
  ): void {

    this.stateSubject.next({
      topics,
    });
  }

}