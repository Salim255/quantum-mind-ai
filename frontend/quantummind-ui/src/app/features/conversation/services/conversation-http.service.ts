import { Injectable } from "@angular/core";
import { environment } from "../../../../environments/environment";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

export interface ConversationPayload {
  user_id: string;
  message: string;
  conversation_id: string;
}

export interface ConversationResponse {
  status: "success",
  data: {
    answer: AnswerPayload;
    memory_updated: boolean;
    conversation_id: string;
  }
}

export interface AnswerPayload {
  query: string;
  retrieved_chunks: string[];
  final_answer: FinalAnswer;
  source: string[];
  latency_ms: number;
}

export interface FinalAnswer {
  answer: string;
  key_points: string[];
  step_by_step: string[];
  analogy: string;
  confidence: number;
  sources: string[];
}

@Injectable({providedIn: "root"})
export class ConversationHttpService {
  private ENV = environment;
  private baseUrl: string = `${this.ENV.apiBaseUrl}/conversations`;

  constructor(private http: HttpClient){}

  sendMessage(payload: ConversationPayload): Observable<ConversationResponse>{
    return this.http.post<ConversationResponse>(`${this.baseUrl}/messages`,payload)
  }
}
