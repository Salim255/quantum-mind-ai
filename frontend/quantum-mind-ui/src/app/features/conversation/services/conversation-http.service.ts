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

  private controller: AbortController | null = null;

  async sendStreamMessage(
    payload: ConversationPayload
  ): Promise<ReadableStreamDefaultReader<Uint8Array> | null> {

    // ------------------------------------------------------------
    // 1. Cancel any previous streaming request
    // ------------------------------------------------------------
    if (this.controller) {
      this.controller.abort();
    }

    // ------------------------------------------------------------
    // 2. Create a fresh controller for THIS request
    // ------------------------------------------------------------
    this.controller = new AbortController();

    let response: Response;

    try {

      response = await fetch(`${this.baseUrl}/messages/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
        signal: this.controller.signal   // 🔥 CRITICAL FIX
      });

    } catch (err) {
      console.error("Fetch failed:", err);
      return null;
    }

    // ------------------------------------------------------------
    // 3. Validate stream body
    // ------------------------------------------------------------
    if (!response.body) return null;

    return response.body.getReader();
  }
}
