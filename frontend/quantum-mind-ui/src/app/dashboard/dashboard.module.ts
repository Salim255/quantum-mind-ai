import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { DashboardPage } from "./dashboard.page";
import { CommonModule } from "@angular/common";
import { DashboardRoutingModule } from "./dashboard-routing.module";
import { HeaderComponent } from "./components/header/header.component";
import { WrapperLayoutComponent } from "./components/wrapper-layout/wrapper-layout.component";
import { AsideLayoutComponent } from "./components/aside-layout/aside-layout.component";
import { BreadCrumbsComponent } from "./components/bread-crumbs/bread-crumbs.component";
import { AsideNavLinkComponent } from "./components/aide-nav-link/aside-nav-link.component";
import { SharedModule } from "../shared/shared.module";
import { AssistantLauncherComponent } from "./components/assistant-launcher/assistant-launcher.component";
import { AssistantPanelComponent } from "../features/ai-assistant/components/assistant-panel/assistant-panel.component";

@NgModule({
  imports: [SharedModule, CommonModule, DashboardRoutingModule],
  declarations: [
    AssistantPanelComponent,
    AssistantLauncherComponent,
    AsideNavLinkComponent,
    BreadCrumbsComponent,
    AsideLayoutComponent,
    WrapperLayoutComponent,
    HeaderComponent,
    DashboardPage
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class DashboardModule {}
