import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { AIAssistantRoutingModule } from "./ai-assistant-routing.module";
import { AIAssistantPage } from "./ai-assistant.page";

@NgModule({
  imports: [CommonModule, AIAssistantRoutingModule],
  declarations: [AIAssistantPage]
})

export class AIAssistantModule {}
