import { RouterModule, Routes } from "@angular/router";
import { AttemptPage } from "./attempt.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path:'',
    component: AttemptPage
  }
]


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class AttemptRoutingModule {}