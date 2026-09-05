import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  Observable,
  map,
  tap,
} from 'rxjs';

import { Attempt, AttemptResponseDTO } from '../interfaces/attempt.interface';

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



  createAttempt(
    topicId: string,
  ): Observable<ApiResponseDTO<AttemptResponseDTO>> {

   return  this.attemptHttpService
      .createAttempt(topicId)
      .pipe(
        tap((response) => {
           this.setAttempt(
            response.data.attempt,
          );
        })
      );
  }


 
  getAttempt(
    attemptId: string,
  ): Observable<ApiResponseDTO<AttemptResponseDTO>> {

    return this.attemptHttpService
      .getAttempt(attemptId).pipe(
        tap(response => {
          this.setAttempt(response.data.attempt);
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