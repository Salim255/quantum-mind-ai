import { Component, signal } from "@angular/core";
import { AssistantMessage } from "../assistant-message/assistant-message.component";
import { ConversationService } from "../../../conversation/services/conversation.service";
import { Conversation } from "../../../conversation/model/conversation.model";
import { Subscription } from "rxjs";
import { MessageService } from "../../../conversation/services/message.service";

export interface AssistantConversation {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}

@Component({
  selector: "app-assistant-conversation",
  templateUrl: "./assistant-conversation.component.html",
  styleUrl: "./assistant-conversation.component.scss",
  standalone: false
})
export class AssistantConversationComponent {
 ASSISTANT_MESSAGES: AssistantMessage[] = [
  {
    id: "msg-001",
    conversationId: "conversation-001",
    role: "user",
    content: "What is quantum entanglement?",
    createdAt: new Date("2026-08-13T09:00:00")
  },
  {
    id: "msg-002",
    conversationId: "conversation-001",
    role: "assistant",
    content:
      "Quantum entanglement is a physical phenomenon where two or more quantum systems become correlated in such a way that their states cannot be described independently. Measuring one system can reveal information about the other, even when they are separated by a large distance.\n\nImportantly, entanglement does not allow information to travel faster than light. The correlations are established by the shared quantum state, while usable classical communication is still limited by the speed of light.",
    createdAt: new Date("2026-08-13T09:00:08")
  },
];
  private conversationSubscription!: Subscription;
  messages = signal<AssistantMessage []>(this.ASSISTANT_MESSAGES);
  private streamResponseSubject!: Subscription;
  private fullResponse: string | null =  null;

  constructor(
    private messageService: MessageService,
    private conservationService: ConversationService
  ){}


  ngOnInit(): void {
    //Called after the constructor, initializing input properties, and the first call to ngOnChanges.
    //Add 'implements OnInit' to the class.
    this.subscribeToConversation();
    this.subscribeToStreamResponse();
  }

  subscribeToConversation(): void{
    this.conversationSubscription = this.conservationService
    .getConversation.subscribe((conversation: Conversation | null) => {
      //this.conversation = conversation;
      //this.messages.set(this.conversation?.getMessages()?? []);
      console.log(conversation, "hello from");
    })
  }


  subscribeToStreamResponse(){
    this.streamResponseSubject = this.messageService
    .getStreamResponse$.subscribe(
      {
        next: (response) => {
            console.log(response)
            // accumulate chunks
            this.fullResponse = response;
            this.ASSISTANT_MESSAGES[1] =  {
                id: "msg-002",
                conversationId: "conversation-001",
                role: "assistant",
                content: this.fullResponse ?? "",
                createdAt: new Date("2026-08-13T09:00:08")
              }

            this.messages.set([...this.ASSISTANT_MESSAGES])
            // convert Markdown → HTML
            //const html =  marked(this.fullResponse ?? "") as string;

            // update your signal
            //this.response.set(html);

            // Why requestAnimationFrame is better:
            // runs after DOM paint
            // more aligned with browser rendering cycle
            // less fragile than timers
            //requestAnimationFrame(() => {
              //MathJax.typesetPromise?.();
            //});

            setTimeout(() => {
              //MathJax.typesetPromise?.();
            }, 0)
        }
      }
    )
  }



  ngOnDestroy(): void {
    //Called once, before the instance is destroyed.
    //Add 'implements OnDestroy' to the class.
    this.conversationSubscription?.unsubscribe();

    this.streamResponseSubject?.unsubscribe();
  }
}
