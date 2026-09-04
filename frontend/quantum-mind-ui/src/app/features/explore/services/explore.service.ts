import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  map,
  Observable,
} from 'rxjs';

import { ExploreHttpService } from './explore-http.service';
import { ExploreState, ExploreQuizDTO } from '../interfaces/explore.dtos';



@Injectable({
  providedIn: 'root',
})
export class ExploreService {

  private readonly stateSubject =
    new BehaviorSubject<ExploreState>({
      quizzes: [],
    });

  private readonly state$ =
    this.stateSubject.asObservable();


  constructor(
    private readonly exploreHttpService: ExploreHttpService,
  ) {}


  fetchTopics(): void {

    this.exploreHttpService
      .getTopics()
      .subscribe({
        next: response => {
          console.log(response);
          this.setTopics(
            response.data.quizzes

          );

        },
      });
  }

  get getTopics$(): Observable<ExploreQuizDTO[]> {

    return this.state$.pipe(
      map(state => state.quizzes),
    );
  }


  private setTopics(
    quizzes: ExploreQuizDTO[],
  ): void {

    this.stateSubject.next({
      quizzes,
    });
  }

}