import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  Observable,
  map,
  tap,
} from 'rxjs';

import { Attempt, AttemptResponseDTO, AttemptUpdateScoreResponseDTO } from '../interfaces/attempt.interface';

import { AttemptHttpService } from './attempt-http.service';
import { ApiResponseDTO } from '../../../shared/interfaces/api-response.dto';


interface AttemptState {
  attempt: Attempt | null;
}


@Injectable({
  providedIn: 'root',
})
export class AttemptService {

  private readonly stateSubject =
    new BehaviorSubject<AttemptState>({
      attempt: null,
    });

  private readonly state$ =
    this.stateSubject.asObservable();


  constructor(
    private readonly attemptHttpService: AttemptHttpService,
  ) {}



  finishAttempt(): Observable<ApiResponseDTO<AttemptResponseDTO>> {
    const attempt = this.attemptValue;

    if (!attempt) {
      throw new Error('Cannot finish attempt: no active attempt');
    }

    return this.attemptHttpService
      .finishAttempt(attempt.id)
      .pipe(
        tap((response) => {
          const updatedAttempt = response.data.attempt;

          this.setAttempt({
            ...attempt,
            score: updatedAttempt.score,
            correct_answers: updatedAttempt.correct_answers,
            is_completed: updatedAttempt.is_completed,
          });
        }),
      );
  }

  submitAnswer(
    answerId: string,
  ): Observable<ApiResponseDTO<AttemptResponseDTO>> {

    const attempt = this.attemptValue;

    if (!attempt) {
      throw new Error('Cannot update score: no active attempt');
    }

    return this.attemptHttpService
      .updateAttemptScore(
        attempt.id,
        answerId,
      )
      .pipe(
        tap((response) => {
          const updatedAttempt = response.data.attempt;
          console.log(updatedAttempt, "hello from coming updated attempt")
          this.setAttempt({
            ...attempt,
            score: updatedAttempt.score,
            correct_answers: updatedAttempt.correct_answers,
            is_completed: updatedAttempt.is_completed,
          });
        }),
      );
  }

  createAttempt(
    topicId: string,
  ): Observable<ApiResponseDTO<AttemptResponseDTO>> {

   return  this.attemptHttpService
      .createAttempt(topicId)
      .pipe(
        tap((response) => {
           this.setAttempt(
            response.data.attempt as Attempt,
          );
        })
      );
  }


  get attemptValue(){
    return this.stateSubject.value?.attempt ?? null
  }

  getAttempt(
    attemptId: string,
  ): Observable<ApiResponseDTO<AttemptResponseDTO>> {

    return this.attemptHttpService
      .getAttempt(attemptId).pipe(
        tap(response => {
          this.setAttempt(response.data.attempt as Attempt);
        })
      )
      ;
  }


 
  get getAttempt$(): Observable<Attempt | null> {

    return this.state$.pipe(
      map(state => state.attempt),
    );
  }


 
  private setAttempt(
    attempt: Attempt,
  ): void {

    this.stateSubject.next({
      attempt,
    });
  }

}