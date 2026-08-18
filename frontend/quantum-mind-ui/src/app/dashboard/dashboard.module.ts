import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { DashboardPage } from "./dashboard.page";
import { CommonModule } from "@angular/common";
import { DashboardRoutingModule } from "./dashboard-routing.module";
import { HeaderComponent } from "./components/header/header.component";
import { WrapperLayoutComponent } from "./components/wrapper-layout/wrapper-layout.component";
import { AsideLayoutComponent } from "./components/aside-layout/aside-layout.component";
import { BreadCrumbsComponent } from "./components/bread-crumbs/bread-crumbs.component";
import { SecondaryAsideNavLinkComponent } from "./components/secondary-aide-nav-link/secondary-aside-nav-link.component";
import { SharedModule } from "../shared/shared.module";
import { AngularSplitModule } from 'angular-split';
import { AIAssistantModule } from "../features/ai-assistant/ai-assistant.module";
import { AsidePrimaryNavComponent } from "./components/aside-primary-nav/aside-primary-nav.component";
import { AsideSecondaryNavComponent } from "./components/aside-secondary-nav/aside-secondary-nav.component";
import { PrimaryAsideNavLinkComponent } from "./components/primary-aide-nav-link/primary-aside-nav-link.component";
import { MobileMenuComponent } from "./components/mobile-menu/mobile-menu.component";

@NgModule({
  imports: [
    AngularSplitModule,
    AIAssistantModule,
    SharedModule,
    CommonModule,
    DashboardRoutingModule
  ],
  declarations: [
     MobileMenuComponent,
    SecondaryAsideNavLinkComponent,
    PrimaryAsideNavLinkComponent,
    AsideSecondaryNavComponent,
    AsidePrimaryNavComponent,
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
