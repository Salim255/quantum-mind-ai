import { Injectable } from "@angular/core";
import { environment } from "../../../../environments/environment";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

export interface ConversationPayload {
  user_id: string;
  message: string;
  conversation_id: string;
}

@Injectable({providedIn: "root"})
export class ConversationHttpService {
  private ENV = environment;
  private baseUrl: string = `${this.ENV}/conversations`;

  constructor(private http: HttpClient){}

  sendMessage(message: string): Observable<any>{
    return this.http.
  }
}
