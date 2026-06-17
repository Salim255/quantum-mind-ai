import { Injectable } from "@angular/core";
import { AnswerPayload, ConversationHttpService, ConversationPayload, ConversationResponse, FinalAnswer } from "./conversation-http.service";
import { BehaviorSubject, Observable, of, tap } from "rxjs";
import { Conversation } from "../model/conversation.model";
import { MessageService } from "./message.service";
import { QuestionService } from "./question.service";

@Injectable({providedIn: "root"})
export class ConversationService {
  private conversationSubject = new BehaviorSubject<Conversation| null>(null);

  constructor(
    private questionService: QuestionService,
    private messageService: MessageService,
    private conversationHttpService: ConversationHttpService,
  ){}

  sendMessage(payload: ConversationPayload): Observable<ConversationResponse>{
    this.questionService.setQuestion(payload.message);
    return this.conversationHttpService.sendMessage(payload).pipe(
      tap((response: ConversationResponse) => {
        const final_answer: FinalAnswer = response?.data.answer?.final_answer;
        const answer_payload: AnswerPayload = response.data.answer;
        this.messageService.setMessage(answer_payload);
      })
    );
  }

  async consumeStream(reader: ReadableStreamDefaultReader<Uint8Array>) {

    const decoder = new TextDecoder();
    let fullText = '';

    while (true) {

      const { value, done } = await reader.read();

      if (done)  {
        this.messageService.completeStreamResponseSubject()
        break;
      }

      const chunk = decoder.decode(value, { stream: true });

      // split SSE messages
      const lines = chunk.split('\n');

      for (const line of lines) {

        if (line.startsWith('data:')) {

          const content = line.replace('data:', '').trim();

          // remove quotes if present
          const cleaned = content
              .replace(/^"|"$/g, '')
              .replace(/\\n/g, '\n');
          // const cleaned = content.replace(/\\n/g, '\n');
          //const cleaned = content.replace(/\n/g, '<br>');
          fullText += cleaned;
          this.messageService.setStreamResponseSubject(fullText);
          //this.aiMessage = fullText;
        }
      }

      //fullText += chunk;
      // 👉 update UI here
      // this.aiMessage = fullText;
    }
    //console.log('accumulated:', fullText);
    reader.releaseLock();
  }

  async sendStreamMessage(
    payload: ConversationPayload
    ):Promise< ReadableStreamDefaultReader<Uint8Array> | null> {
      this.questionService.setQuestion(payload.message);
      const response =  await this.conversationHttpService.sendStreamMessage(payload)

      if(response){
        this.consumeStream(response);
      }
      return response
  }

  setConversation(conversation: Conversation){
    this.conversationSubject.next(conversation);
  }

  fetChConversation():Observable<Conversation>{
    const conversation = new Conversation(
            'conv-1',
              'user-1',
              []
            );

    return of(conversation).pipe(
      tap((conversation: Conversation) => {
        this.setConversation(conversation);
      })
    );
  }

  get getConversation(): Observable<Conversation | null> {
    return this.conversationSubject.asObservable();
  }


  appendMessage(){}
}
