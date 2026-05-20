import { NgModule } from "@angular/core";
import { ConversationPage } from "./conversation.page";
import { ConversationRoutingModule } from "./conversation-routing.module";
import { CommonModule } from "@angular/common";
import { MessagesComponent } from "./components/messages/messages.component";

@NgModule({
  imports: [
    CommonModule,
    ConversationRoutingModule,
  ],
  declarations: [
    MessagesComponent,
    ConversationPage],
})
export class ConversationModule {}
