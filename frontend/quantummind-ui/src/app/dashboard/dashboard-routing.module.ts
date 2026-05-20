import { RouterModule, Routes } from "@angular/router";
import { DashboardPage } from "./dashboard.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: DashboardPage,
    children: [
      {
        path: "/conversation",
        loadChildren: () => import("../features/conversation/conversation.module").then(m => m.ConversationModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DashboardRoutingModule {}
