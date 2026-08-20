import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { ProgressPage } from "./progress.page";
import { ProgressRoutingModule } from "./progress-routing.module";
import { ProgressHeaderComponent } from "./components/progress-header/progress-header.component";
import { ProgressSnapshotComponent } from "./components/progress-snapshot/progress-snapshot.component";
import { ProgressKnowledgeComponent } from "./components/progress-knowledge/progress-knowledge.component";
import { ProgressKnowledgeCardComponent } from "./components/progress-knowledge-card/progress-knowledge-card.component";
import { ProgressActivityComponent } from "./components/progress-activity/progress-activity.component";
import { ProgressInsightCardComponent } from "./components/progress-insight-card/progress-insight-card.component";
import { ProgressInsightsComponent } from "./components/progress-insights/progress-insights.component";
import { ProgressAchievementsComponent } from "./components/progress-achievements/progress-achievements.component";
import { ProgressAchievementCardComponent } from "./components/progress-achievement-card/progress-achievement-card.component";

@NgModule({
  imports: [
    CommonModule,
    ProgressRoutingModule,
  ],
  declarations: [
    ProgressAchievementCardComponent,
    ProgressAchievementsComponent,
    ProgressInsightsComponent,
    ProgressInsightCardComponent,
    ProgressActivityComponent,
    ProgressKnowledgeCardComponent,
    ProgressKnowledgeComponent,
    ProgressSnapshotComponent,
    ProgressHeaderComponent,
    ProgressPage
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class ProgressModule {}
