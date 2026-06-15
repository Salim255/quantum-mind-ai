import { RouterModule, Routes } from "@angular/router";
import { LearnPage } from "./learn.page";
import { NgModule } from "@angular/core";
import { LearnHomePage } from "./pages/learn-home-page/learn-home.page";

const routes: Routes = [
  {
    path: "",
    component: LearnPage,
    children: [
      {
        path: "",
        component: LearnHomePage
      },
      {
        path: "spin",
        loadChildren: () => import("./pages/spin/spin.module").then((m) => m.SpinModule)
      },
      {
        path: "linear-algebra",
        loadChildren: () => import("./pages/mathematics/mathematics.module").then(m => m.MathematicsModule)
      },
      {
        path: "physics",
        loadChildren: () => import("./pages/physics/physics.module").then(m => m.PhysicsModule)
      },
      {
        path: "quantum-computing",
        loadChildren: () => import("./pages/quantum-computing/quantum-computing.module").then(m => m.QuantumComputingModule)
      },
      {
        path: "algorithms",
        loadChildren: () => import("./pages/algorithms/algorithms.module").then(m => m.AlgorithmsModule)
      }
    ]
  },
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class LearnRoutingModule {}
