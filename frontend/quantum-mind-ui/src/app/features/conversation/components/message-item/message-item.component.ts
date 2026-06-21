import {
  Component,
  Input,
  NgZone,
  OnChanges,
  OnDestroy,
  OnInit,
  signal,
  SimpleChanges
} from "@angular/core";
import { marked } from 'marked';
import { FinalAnswer } from "../../services/conversation-http.service";
import { MessageService } from "../../services/message.service";
import { Subscription } from "rxjs";

declare const MathJax: any;

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

  constructor(
    private ngZone: NgZone,
    private messageService: MessageService,
  ){}

  ngOnInit(): void {
    this.subscribeToStreamResponse();
    // Wait for Angular to finish rendering//
    requestAnimationFrame(() => {
      MathJax.typesetPromise?.();
    });
}

  ngOnChanges(changes: SimpleChanges): void {
    if(changes) {
      console.log(this.message);
    }
  }

  subscribeToStreamResponse(){
    this.streamResponseSubject = this.messageService
    .getStreamResponse$.subscribe(
      {
        next: (response) => {

            // accumulate chunks
            this.fullResponse = response;

            // convert Markdown → HTML
            const html =  marked(this.fullResponse ?? "") as string;

            // update your signal
            this.response.set(html);

            // Why requestAnimationFrame is better:
            // runs after DOM paint
            // more aligned with browser rendering cycle
            // less fragile than timers
            requestAnimationFrame(() => {
              MathJax.typesetPromise?.();
            });
        }
      }
    )
  }

  ngOnDestroy(): void {
    this.streamResponseSubject?.unsubscribe();
  }
}
