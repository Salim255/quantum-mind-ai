import { Injectable } from "@angular/core";
import { environment } from "../../../../environments/environment";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

export interface ConversationPayload {
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
  private baseUrl: string = `${this.ENV.apiBaseUrl}/rag`;

  constructor(private http: HttpClient){}

  sendMessage(payload: ConversationPayload): Observable<ConversationResponse>{
    return this.http.post<ConversationResponse>(`${this.baseUrl}/messages`,payload)
  }

  sendStreamMessage(
    payload: ConversationPayload
  ): Observable<string> {

    return new Observable(observer => {

      const controller = new AbortController();

      fetch(`${this.baseUrl}/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
        signal: controller.signal
      })
      .then(async response => {
    
        // If no streaming body → cannot stream
        if (!response.body) {
          observer.error(new Error('No response body'));
          return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullText = '';

        try {

          while (true) {

            const { done, value } = await reader.read();

            // Stream ended normally
            if (done) {
              observer.complete();
              break;
            }

            const chunk = decoder.decode(value, {
              stream: true
            });

            // SSE events come line-by-line
            for (const line of chunk.split('\n')) {

              if (!line.startsWith('data:')) continue;

              const raw = line.replace('data:', '').trim();

              // Try to parse JSON SSE events
              let parsed: any;
              try {
                parsed = JSON.parse(raw);
              } catch {
                parsed = raw; // fallback for plain text
              }

              // If backend sent an error event → propagate to Angular error()
              if (parsed && parsed.error) {
                observer.error(parsed.error);
                return; // stop reading further chunks
              }

              // Normal chunk → accumulate and emit
              const cleaned =
                typeof parsed === 'string'
                ?
                parsed.replace(/^"|"$/g, '').replace(/\\n/g, '\n')
                : parsed;

              fullText += cleaned;

              observer.next(fullText);
            }

          }

        } catch (err) {
          console.log("error", err)
          observer.error(err);
        }

      })
      .catch(err => observer.error(err));
    });
  }
}
