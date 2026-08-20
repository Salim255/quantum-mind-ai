import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { OverviewRoutingModule } from "./practice-overview-routing.module";
import { PracticeOverviewPage } from "./practice-overview.page";
import { PracticeOverviewHeaderComponent } from "./components/practice-overview-header/practice-overview-header.component";

@NgModule({
  imports: [
    CommonModule,
    OverviewRoutingModule
  ],
  declarations: [
    PracticeOverviewHeaderComponent,
    PracticeOverviewPage
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class PracticeOverviewModule {}
