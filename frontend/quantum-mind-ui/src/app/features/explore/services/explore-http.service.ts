import { Injectable } from "@angular/core";
import { environment } from "../../../../environments/environment";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { ApiResponseDTO } from "../../../shared/interfaces/api-response.dto";
import { ExploreState } from "../interfaces/explore.dtos";

@Injectable({providedIn: 'root'})
export class ExploreHttpService {

    private ENV = environment
    private baseUrl = `${this.ENV.apiBaseUrl}/explore/quizzes`
    constructor(private http: HttpClient){}
  

    getTopics(): Observable<ApiResponseDTO<ExploreState>> {
      return this.http.get<ApiResponseDTO<ExploreState>>(
        `${this.baseUrl}`,
        {
          params: {
            include_sections: false,
            include_blocks: false,
          },
        },
      );
    }
}