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
        path: "spin-qubits",
        loadChildren: () => import("./pages/spin-and-qubits/spin-qubits.module").then(m => m.SpinQubitsModule)
      },
      {
        path: "entanglement",
        loadChildren: () => import("./pages/entanglement/entanglement.module").then((m) => m.EntanglementModule)
      },
      {
        path: "bell-Inequality",
        loadChildren: () => import("./pages/bell-inequality/bell-inequality.module").then((m) => m.BellInequalityModule)
      },
      {
        path: "classical-logic",
        loadChildren: () => import("./pages/classical-logic/classical-logic.module").then((m) => m.ClassicalLogicModule)
      },

      {
        path: "quantum-logic",
        loadChildren: () => import("./pages/quantum-logic/quantum-logic.module").then(m => m.QuantumLogicModule)
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
