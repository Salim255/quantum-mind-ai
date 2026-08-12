import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { AIAssistantPage } from "./ai-assistant.page";
import { AssistantHeaderComponent } from "./components/assistant-header/assistant-header.component";
import { AssistantPanelComponent } from "./components/assistant-panel/assistant-panel.component";
import { AssistantFooterComponent } from "./components/assistant-footer/assistant-footer.component";
import { AssistantLauncherComponent } from "./components/assistant-launcher/assistant-launcher.component";
import { AssistantConversationComponent } from "./components/assistant-conversation/assistant-conversation.component";
import { AssistantComposerComponent } from "./components/assistant-composer/assistant-composer.component";

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [
    AssistantComposerComponent,
    AssistantConversationComponent,
    AssistantLauncherComponent,
    AssistantFooterComponent,
    AssistantHeaderComponent,
    AssistantPanelComponent,
    AIAssistantPage
   ],
  exports: [
    AIAssistantPage,
    AssistantLauncherComponent
  ]
})

export class AIAssistantModule {}
