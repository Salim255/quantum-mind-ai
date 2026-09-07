import { RouterModule, Routes } from "@angular/router";
import { AttemptResultPage } from "./attempt-result.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: AttemptResultPage
  }
]


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AttemptResultRoutingModule {}