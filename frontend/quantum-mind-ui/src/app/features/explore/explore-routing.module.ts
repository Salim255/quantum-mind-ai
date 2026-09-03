import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { ExplorePage } from "./explore.page";
import { ExploreHomeComponent } from "./components/explore-home/explore-home.component";

const routes: Routes = [
  {
    path: "",
    component: ExplorePage,
    children: [
      {
        path: "",
        component: ExploreHomeComponent
      },
      {
        path: "attempt",
        loadChildren: () => import("../attempt/attempt.module").then((m) => m.AttemptModule),
      }
    ]
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class ExploreRoutingModule{}
