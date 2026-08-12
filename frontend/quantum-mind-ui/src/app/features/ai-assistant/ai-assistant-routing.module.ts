import { RouterModule, Routes } from "@angular/router";
import { AIAssistantPage } from "./ai-assistant.page";
import { NgModule } from "@angular/core";

const routes: Routes = [{
  path: '',
  component: AIAssistantPage
}]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class AIAssistantRoutingModule {}
