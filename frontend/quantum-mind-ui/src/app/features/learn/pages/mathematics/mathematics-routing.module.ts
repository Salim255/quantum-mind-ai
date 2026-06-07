import { RouterModule, Routes } from "@angular/router";
import { MathematicsPage } from "./mathematics.page";
import { NgModule } from "@angular/core";

const routes: Routes = [
  {
    path: "",
    component: MathematicsPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MathematicsRoutingModule {}
