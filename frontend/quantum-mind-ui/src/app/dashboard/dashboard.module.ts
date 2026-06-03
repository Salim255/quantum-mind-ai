import { NgModule } from "@angular/core";
import { DashboardPage } from "./dashboard.page";
import { CommonModule } from "@angular/common";
import { DashboardRoutingModule } from "./dashboard-routing.module";
import { HeaderComponent } from "./components/header/header.component";
import { WrapperLayoutComponent } from "./components/wrapper-layout/wrapper-layout.component";
import { AsideLayoutComponent } from "./components/aside-layout/aside-layout.component";

@NgModule({
  imports: [CommonModule, DashboardRoutingModule],
  declarations: [
    AsideLayoutComponent,
    WrapperLayoutComponent,
    HeaderComponent,
    DashboardPage
  ],
})
export class DashboardModule {}
