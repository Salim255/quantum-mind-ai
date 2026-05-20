import { NgModule } from "@angular/core";
import { DashboardPage } from "./dashboard.page";
import { CommonModule } from "@angular/common";
import { DashboardRoutingModule } from "./dashboard-routing.module";

@NgModule({
  imports: [CommonModule, DashboardRoutingModule],
  declarations: [DashboardPage],
})
export class DashboardModule {}
