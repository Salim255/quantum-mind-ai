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

  /*
   * ==========================================================
   * STATE
   * ==========================================================
   *
   * The Attempt feature only needs one piece of state:
   *
   *   attempt
   *
   * The API remains the source of truth.
   *
   * We initialize the state with null because no attempt
   * has been created or loaded yet.
   */
  private readonly stateSubject =
    new BehaviorSubject<AttemptState>({
      attempt: null,
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
    private readonly attemptHttpService: AttemptHttpService,
  ) {}


  /*
   * ==========================================================
   * CREATE ATTEMPT
   * ==========================================================
   *
   * Creates a new attempt for the given topic.
   *
   * The HTTP service is responsible only for communicating
   * with the API.
   *
   * This service is responsible for taking the API response
   * and updating the Attempt state.
   */
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


  /*
   * ==========================================================
   * GET ATTEMPT
   * ==========================================================
   *
   * Retrieves an existing attempt by its ID and stores it
   * in the Attempt state.
   */
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


  /*
   * ==========================================================
   * GET ATTEMPT
   * ==========================================================
   *
   * Returns the attempt currently stored in the state.
   *
   * Components receive the complete Attempt object returned
   * by the API.
   */
  get getAttempt$(): Observable<Attempt | null> {

    return this.state$.pipe(
      map(state => state.attempt),
    );
  }


  /*
   * ==========================================================
   * SET ATTEMPT
   * ==========================================================
   *
   * Updates the Attempt state.
   *
   * Kept private so that only this service controls
   * state mutation.
   */
  private setAttempt(
    attempt: Attempt,
  ): void {

    this.stateSubject.next({
      attempt,
    });
  }

}