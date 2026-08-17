import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { OverviewRoutingModule } from "./overview-routing.module";
import { OverviewPage } from "./overview.page";

@NgModule({
  imports: [
    CommonModule,
    OverviewRoutingModule
  ],
  declarations: [OverviewPage]
})
export class OverviewModule {}
