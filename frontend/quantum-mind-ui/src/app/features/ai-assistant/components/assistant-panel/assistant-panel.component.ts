import {
  Component,
  OnDestroy,
  OnInit,
  output,
  signal,
} from '@angular/core';
import { ConversationService } from '../../../conversation/services/conversation.service';
import { Subscription } from 'rxjs';
import { AssistantMessage } from '../assistant-message/assistant-message.component';

@Component({
  selector: 'app-assistant-panel',
  templateUrl: './assistant-panel.component.html',
  styleUrl: './assistant-panel.component.scss',
  standalone: false
})
export class AssistantPanelComponent implements OnInit, OnDestroy {
  private conversationSubscription!: Subscription;
  readonly close = output<void>();
  messages = signal<AssistantMessage[]>([]);

  constructor(private conversationService: ConversationService){}

  ngOnInit(): void {
    this.subscribeToConversation();
  }

  subscribeToConversation(){
    this.conversationSubscription = this.conversationService
    .getConversation
    .subscribe(conversation => {
      console.log(conversation),"hello from conversation";
      this.messages.set(conversation?.getMessages() ?? []);
    })
  }

  protected onClose(): void {
    this.close.emit();
  }

  ngOnDestroy(): void {
    this.conversationSubscription?.unsubscribe();
  }
}
