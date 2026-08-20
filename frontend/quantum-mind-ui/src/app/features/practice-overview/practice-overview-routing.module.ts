import { RouterModule, Routes } from "@angular/router";
import { PracticeOverviewPage } from "./practice-overview.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: PracticeOverviewPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OverviewRoutingModule {}
