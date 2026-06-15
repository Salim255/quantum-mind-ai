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
