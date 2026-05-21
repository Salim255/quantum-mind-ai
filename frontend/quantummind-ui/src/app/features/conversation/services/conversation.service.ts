import { Injectable } from "@angular/core";
import { ConversationHttpService, ConversationPayload } from "./conversation-http.service";
import { Observable } from "rxjs";

@Injectable({providedIn: "root"})
export class ConversationService {
  constructor(private conversationHttpService: ConversationHttpService){}


  sendMessage(payload: ConversationPayload): Observable<any>{
     return  this.conversationHttpService.sendMessage(payload);
  }
}
