import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { OverviewRoutingModule } from "./practice-overview-routing.module";
import { PracticeOverviewPage } from "./practice-overview.page";
import { PracticeOverviewHeaderComponent } from "./components/practice-overview-header/practice-overview-header.component";
import { PracticeOverviewSnapshotComponent } from "./components/practice-overview-snapshot/practice-overview-snapshot.component";
import { PracticeOverviewMetricCardComponent } from "./components/practice-overview-metric-card/practice-overview-metric-card.component";
import { PracticeOverviewSectionComponent } from "./components/practice-overview-section/practice-overview-section.component";
import { PracticeOverviewTopicCardComponent } from "./components/practice-overview-topic-card/practice-overview-topic-card.component";
import { PracticeOverviewProgressComponent } from "./components/practice-overview-progress/practice-overview-progress.component";
import { PracticeOverviewProgressCardComponent } from "./components/practice-overview-progress-card/practice-overview-progress-card.component";

@NgModule({
  imports: [
    CommonModule,
    OverviewRoutingModule
  ],
  declarations: [
    PracticeOverviewProgressCardComponent,
    PracticeOverviewProgressComponent,
    PracticeOverviewTopicCardComponent,
    PracticeOverviewSectionComponent,
    PracticeOverviewMetricCardComponent,
    PracticeOverviewSnapshotComponent,
    PracticeOverviewHeaderComponent,
    PracticeOverviewPage
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class PracticeOverviewModule {}
