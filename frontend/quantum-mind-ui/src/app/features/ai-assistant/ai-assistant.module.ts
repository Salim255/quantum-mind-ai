import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { AIAssistantRoutingModule } from "./ai-assistant-routing.module";
import { AIAssistantPage } from "./ai-assistant.page";
import { AssistantHeaderComponent } from "./components/assistant-header/assistant-header.component";
import { AssistantPanelComponent } from "./components/assistant-panel/assistant-panel.component";

@NgModule({
  imports: [CommonModule, AIAssistantRoutingModule],
  declarations: [
    AIAssistantPage,
    AssistantHeaderComponent,
    AssistantPanelComponent
   ]
})

export class AIAssistantModule {}
