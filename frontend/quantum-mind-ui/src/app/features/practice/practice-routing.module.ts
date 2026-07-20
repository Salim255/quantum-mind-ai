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
        path: "quizzes",
        loadChildren: () => import("./pages/quiz-page/quiz.module").then((m) => m.QuizModule)
      }
    ]
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class PracticeRoutingModule {}
