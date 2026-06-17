import { Component, Input, OnChanges, OnDestroy, OnInit, signal, SimpleChanges } from "@angular/core";
import { MessageSchema } from "../../model/conversation.model";
import { marked } from 'marked';
import { FinalAnswer } from "../../services/conversation-http.service";
import { MessageService } from "../../services/message.service";
import { Subscription } from "rxjs";

@Component({
  selector: "app-message-item",
  templateUrl: "./message-item.component.html",
  styleUrl: "./message-item.component.scss",
  standalone: false
})

export class MessageItemComponent implements OnInit, OnChanges, OnDestroy {

  @Input() message: FinalAnswer | undefined;
  private streamResponseSubject!: Subscription;
  response = signal<string>("")
  private fullResponse: string | null =  null;

  constructor(private messageService: MessageService){}

  ngOnInit(): void {
    this.subscribeToStreamResponse();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if(changes) {
      console.log(this.message);
    }
  }

  subscribeToStreamResponse(){
    this.streamResponseSubject = this.messageService.getStreamResponse$.subscribe(
      async response => {
        // accumulate chunks
        this.fullResponse = response;

        // convert Markdown → HTML
        const html = await marked(this.fullResponse ?? "");

        // update your signal
        this.response.set(html);

        // optional: render MathJax for equations
        // MathJax.typesetPromise();
      }
    )
  }

  ngOnDestroy(): void {
    this.streamResponseSubject?.unsubscribe();
  }
}
