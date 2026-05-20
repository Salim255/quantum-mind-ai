import { NgModule } from "@angular/core";
import { ConversationPage } from "./conversation.page";
import { ConversationRoutingModule } from "./conversation-routing.module";
import { CommonModule } from "@angular/common";
import { MessagesComponent } from "./components/messages/messages.component";
import { QuestionMessageItemComponent } from "./components/question-message-item/question-message-item.component";
import { MessageFormComponent } from "./components/message-form/message-form.component";

@NgModule({
  imports: [
    CommonModule,
    ConversationRoutingModule,
  ],
  declarations: [
    MessageFormComponent,
    QuestionMessageItemComponent,
    MessagesComponent,
    ConversationPage],
})
export class ConversationModule {}
