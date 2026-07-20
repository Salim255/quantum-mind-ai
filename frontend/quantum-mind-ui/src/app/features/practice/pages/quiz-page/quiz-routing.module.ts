import { RouterModule, Routes } from "@angular/router";
import { QuizPage } from "./quiz-page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path:"",
    component: QuizPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class QuizRoutingModule{}
