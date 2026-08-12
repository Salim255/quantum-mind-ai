import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { AIAssistantPage } from "./ai-assistant.page";
import { AssistantHeaderComponent } from "./components/assistant-header/assistant-header.component";
import { AssistantPanelComponent } from "./components/assistant-panel/assistant-panel.component";
import { AssistantFooterComponent } from "./components/assistant-footer/assistant-footer.component";

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [
    AssistantFooterComponent,
    AssistantHeaderComponent,
    AssistantPanelComponent,
    AIAssistantPage
   ],
  exports: [AIAssistantPage]
})

export class AIAssistantModule {}
