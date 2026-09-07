import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../../environments/environment';

import { Attempt, AttemptResponseDTO, AttemptUpdateScoreDTO, AttemptUpdateScoreResponseDTO } from '../interfaces/attempt.interface';
import { ApiResponseDTO } from '../../../shared/interfaces/api-response.dto';


@Injectable({
  providedIn: 'root',
})
export class AttemptHttpService {

  private ENV = environment;

  private  baseUrl = `${this.ENV.apiBaseUrl}/attempts`;


  constructor(private http: HttpClient) {}


  finishAttempt(
      attemptId: string,
    ): Observable<ApiResponseDTO<AttemptUpdateScoreResponseDTO>> {

      const url =
        `${this.baseUrl}/${attemptId}/finish`;

      return this.http.patch<
        ApiResponseDTO<AttemptUpdateScoreResponseDTO>
      >(
        url,
        {},
      );
  }
  // ============================================================
  // UPDATE ATTEMPT SCORE
  // ============================================================

  updateAttemptScore(
    attemptId: string,
    answerId: string,
  ): Observable<
    ApiResponseDTO<AttemptUpdateScoreResponseDTO>
  > {

    const url =
      `${this.baseUrl}/${attemptId}/score`;

    const payload: AttemptUpdateScoreDTO = {
      attempt_id: attemptId,
      answer_id: answerId,
    };


    return this.http.patch<
      ApiResponseDTO<AttemptUpdateScoreResponseDTO>
    >(
      url,
      payload,
    );
  }

  createAttempt(
    topicId: string
  ): Observable<ApiResponseDTO<AttemptResponseDTO>> {

    return this.http.post<ApiResponseDTO<AttemptResponseDTO>>(
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
    attemptId: string
  ): Observable<ApiResponseDTO<AttemptResponseDTO>> {

    return this.http
    .get<ApiResponseDTO<AttemptResponseDTO>>(
      `${this.baseUrl}/${attemptId}`
    );
  }

}