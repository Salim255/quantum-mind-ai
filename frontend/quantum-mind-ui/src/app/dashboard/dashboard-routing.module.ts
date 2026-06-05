import { RouterModule, Routes } from "@angular/router";
import { DashboardPage } from "./dashboard.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: DashboardPage,
    children: [
      {
        path: "",
        loadChildren: () => import("../features/conversation/conversation.module").then(m => m.ConversationModule)
      },
      {
        path: "learn",
        loadChildren: () => import("../features/learn/learn.module").then(m => m.LearnModule)
      },
      {
        path: "explore",
        loadChildren: () => import("../features/explore/explore.module").then(m => m.ExploreModule)
      },
      {
        path: "practice",
        loadChildren: () => import("../features/practice/practice.module").then(m => m.PracticeModule)
      },
      {
        path: "progress",
        loadChildren: () => import("../features/progress/progress.module").then(m => m.ProgressModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DashboardRoutingModule {}
