import { Injectable } from "@angular/core";
import { AnswerPayload, ConversationHttpService, ConversationPayload, ConversationResponse, FinalAnswer } from "./conversation-http.service";
import { BehaviorSubject, Observable, of, tap } from "rxjs";
import { Conversation } from "../model/conversation.model";
import { MessageService } from "./message.service";
import { QuestionService } from "./question.service";

@Injectable({providedIn: "root"})
export class ConversationService {
  private conversationSubject = new BehaviorSubject<Conversation| null>(null);
  private currentReader: ReadableStreamDefaultReader<Uint8Array> | null = null;
  private isStreaming = false;

  constructor(
    private questionService: QuestionService,
    private messageService: MessageService,
    private conversationHttpService: ConversationHttpService,
  ){}

  sendMessage(payload: ConversationPayload): Observable<ConversationResponse>{

    this.questionService.setQuestion(payload.message);
    return this.conversationHttpService.sendMessage(payload).pipe(
      tap((response: ConversationResponse) => {
        const answer_payload: AnswerPayload = response.data.answer;
        this.messageService.setMessage(answer_payload);
      })
    );
  }

  /**
   * This function ONLY reads the stream.
   * It must NOT decide lifecycle or cleanup.
   */
  async consumeStream(reader: ReadableStreamDefaultReader<Uint8Array>) {

    const decoder = new TextDecoder();
    let fullText = '';

    try {

      while (true) {

        const { value, done } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value, { stream: true });

        for (const line of chunk.split('\n')) {

          if (!line.startsWith('data:')) continue;

          const content = line.replace('data:', '').trim();

          const cleaned = content
            .replace(/^"|"$/g, '')
            .replace(/\\n/g, '\n');

          fullText += cleaned;

          this.messageService.setStreamResponseSubject(fullText);
        }
      }

    } catch (err) {
      console.error("Stream error:", err);

    } finally {
      // ONLY notify UI
      this.messageService.completeStreamResponseSubject();
    }
  }

  async stopStream() {

    if (!this.currentReader) return;

    try {
      await this.currentReader.cancel();
    } catch {}

    try {
      this.currentReader.releaseLock();
    } catch {}

    this.currentReader = null;
    this.isStreaming = false;
  }

  async sendStreamMessage(payload: ConversationPayload): Promise<void> {

    // ------------------------------------------------------------
    // 1. ALWAYS stop previous stream FIRST
    // ------------------------------------------------------------
    await this.stopStream();

    this.isStreaming = true;

    this.questionService.setQuestion(payload.message);

    const response = await this.conversationHttpService.sendStreamMessage(payload);

    if (!response) {
      this.isStreaming = false;
      return;
    }

    this.currentReader = response;

    try {
      await this.consumeStream(response);
    } finally {
      this.isStreaming = false;
      this.currentReader = null;
    }
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
