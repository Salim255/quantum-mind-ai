import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from "../../../../environments/environment";
import { TopicsResponseDTO } from "../interfaces/topics-response.dto";
import { ApiResponseDTO } from "../../../shared/interfaces/api-response.dto";

@Injectable({providedIn: "root"})
export class LearnHttpService {
  private ENV = environment
  private baseUrl = `${this.ENV.apiBaseUrl}/learns`
  constructor(private http: HttpClient){}

  getDocs(formData: FormData): Observable<any>{
    return this.http.post<any>(`${this.baseUrl}/ingest-pdf`, formData)
  }

  getLearnTopics(): Observable<ApiResponseDTO<TopicsResponseDTO>>{
    return this.http.get<any>(`${this.ENV.apiBaseUrl}/topics`)
  }
}
