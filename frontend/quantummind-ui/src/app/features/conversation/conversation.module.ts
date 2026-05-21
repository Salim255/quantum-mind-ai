import { NgModule } from "@angular/core";
import { FormsModule} from "@angular/forms"
import { ConversationPage } from "./conversation.page";
import { ConversationRoutingModule } from "./conversation-routing.module";
import { CommonModule } from "@angular/common";
import { MessagesComponent } from "./components/messages/messages.component";
import { QuestionMessageItemComponent } from "./components/question-message-item/question-message-item.component";
import { MessageFormComponent } from "./components/message-form/message-form.component";
import { QuestionComponent } from "./components/question/question.component";
import { MessageItemComponent } from "./components/message-item/message-item.component";

@NgModule({
  imports: [
     FormsModule,
    CommonModule,
    ConversationRoutingModule,
  ],
  declarations: [
    MessageItemComponent,
    QuestionComponent,
    MessageFormComponent,
    QuestionMessageItemComponent,
    MessagesComponent,
    ConversationPage],
})
export class ConversationModule {}
