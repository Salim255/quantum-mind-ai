import { NgModule } from "@angular/core";
import { DashboardPage } from "./dashboard.page";
import { CommonModule } from "@angular/common";
import { DashboardRoutingModule } from "./dashboard-routing.module";
import { HeaderComponent } from "./components/header/header.component";

@NgModule({
  imports: [CommonModule, DashboardRoutingModule],
  declarations: [HeaderComponent, DashboardPage],
})
export class DashboardModule {}
