import { NgModule } from "@angular/core";
import { DashboardPage } from "./dashboard.page";
import { CommonModule } from "@angular/common";
import { DashboardRoutingModule } from "./dashboard-routing.module";
import { HeaderComponent } from "./components/header/header.component";
import { WrapperLayoutComponent } from "./components/wrapper-layout/wrapper-layout.component";
import { AsideLayoutComponent } from "./components/aside-layout/aside-layout.component";
import { BreadCrumbsComponent } from "./components/bread-crumbs/bread-crumbs.component";
import { AsideNavLinkComponent } from "./components/aide-nav-link/aside-nav-link.component";

@NgModule({
  imports: [CommonModule, DashboardRoutingModule],
  declarations: [
    AsideNavLinkComponent,
    BreadCrumbsComponent,
    AsideLayoutComponent,
    WrapperLayoutComponent,
    HeaderComponent,
    DashboardPage
  ],
})
export class DashboardModule {}
