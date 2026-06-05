import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { LearnPage } from "./learn.page";
import { LearnRoutingModule } from "./learn-routing.module";

@NgModule({
  imports: [CommonModule, LearnRoutingModule],
  declarations: [LearnPage]
})
export class LearnModule {}
