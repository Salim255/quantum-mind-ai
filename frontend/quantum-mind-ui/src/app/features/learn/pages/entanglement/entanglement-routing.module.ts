import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { EntanglementPage } from "./entanglement.page";

const routes: Routes = [
  {
    path: "",
    component: EntanglementPage
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class EntanglementRoutingModule {}
