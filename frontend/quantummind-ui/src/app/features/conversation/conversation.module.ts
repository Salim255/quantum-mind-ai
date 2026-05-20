import { NgModule } from "@angular/core";
import { ConversationPage } from "./conversation.page";
import { ConversationRoutingModule } from "./conversation-routing.module";
import { CommonModule } from "@angular/common";

@NgModule({
  imports: [
    CommonModule,
    ConversationRoutingModule,
  ],
  declarations: [ConversationPage],
})
export class ConversationModule {}
