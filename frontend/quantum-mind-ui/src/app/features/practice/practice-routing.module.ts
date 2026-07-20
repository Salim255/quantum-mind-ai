import { RouterModule, Routes } from "@angular/router";
import { PracticePage } from "./practice.page";
import { NgModule } from "@angular/core";

const routes:Routes = [
  {
    path: "",
    component: PracticePage,
   /*  children: [
      {
        path: "quizes"
      }
    ] */
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class PracticeRoutingModule {}
