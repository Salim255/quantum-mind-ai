import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../../environments/environment';

import { Attempt } from '../interfaces/attempt.interface';


@Injectable({
  providedIn: 'root',
})
export class AttemptHttpService {

  private ENV = environment;

  private  baseUrl = `${this.ENV.apiBaseUrl}/attempts`;


  constructor( private http: HttpClient) {}


  /*
   * ==========================================================
   * CREATE ATTEMPT
   * ==========================================================
   *
   * Creates a new attempt for a topic.
   *
   * The topic is identified by its ID and is sent
   * as the request body.
   *
   * POST /attempts
   *
   * Body:
   * {
   *   topic_id: string
   * }
   */
  createAttempt(
    topicId: string,
  ): Observable<Attempt> {

    return this.http.post<Attempt>(
      this.baseUrl,
      {
        topic_id: topicId,
      },
    );
  }


  /*
   * ==========================================================
   * GET ATTEMPT
   * ==========================================================
   *
   * Retrieves an existing attempt by its ID.
   *
   * GET /attempts/:id
   */
  getAttempt(
    attemptId: string,
  ): Observable<Attempt> {

    return this.http.get<Attempt>(
      `${this.baseUrl}/${attemptId}`,
    );
  }

}