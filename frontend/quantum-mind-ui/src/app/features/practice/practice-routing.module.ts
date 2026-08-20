import { RouterModule, Routes } from "@angular/router";
import { PracticePage } from "./practice.page";
import { NgModule } from "@angular/core";
import { PracticeHomeComponent } from "./components/practice-home/practice-home.component";


const routes:Routes = [
  {
    path: "",
    component: PracticePage,
    children: [
      {
        path: "",
        component: PracticeHomeComponent
      },
      {
        path: "overview",
        loadChildren: () => import("../practice-overview/practice-overview.module").then((m) => m.PracticeOverviewModule)
      },
      {
        path: "explore",
        loadChildren: () => import("../explore/explore.module").then((m) => m.ExploreModule)
      }
    ]
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class PracticeRoutingModule {}
