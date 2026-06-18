import { AfterViewInit, Component, Input, NgZone, OnChanges, OnDestroy, OnInit, signal, SimpleChanges } from "@angular/core";
import { MessageSchema } from "../../model/conversation.model";
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

export class MessageItemComponent implements OnInit, OnChanges, AfterViewInit, OnDestroy {

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
        },

        complete: () => {
            // optional: render MathJax for equations
            //MathJax.typesetPromise();
            console.log("Its complete")
            setTimeout(() => {
              MathJax.typesetPromise();
            }, 0);
        }
      }
    )
  }

   ngAfterViewInit() {
    // Wait for Angular to finish rendering//
    this.ngZone.onStable.subscribe(() => {
      if (MathJax?.typesetPromise) {
        MathJax.typesetPromise();
      }
    });
  }

  ngOnDestroy(): void {
    this.streamResponseSubject?.unsubscribe();
  }
}
