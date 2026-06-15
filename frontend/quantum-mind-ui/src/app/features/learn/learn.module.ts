import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { LearnPage } from "./learn.page";
import { LearnRoutingModule } from "./learn-routing.module";
import { LearnHomePage } from "./pages/learn-home-page/learn-home.page";
import { SharedModule } from "../../shared/shared.module";


@NgModule({
  imports: [SharedModule, CommonModule, LearnRoutingModule],
  declarations: [LearnPage, LearnHomePage]
})
export class LearnModule {}
