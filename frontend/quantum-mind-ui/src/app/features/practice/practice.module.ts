import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { PracticePage } from "./practice.page";
import { PracticeRoutingModule } from "./practice-routing.module";
import { PracticeHomeComponent } from "./components/practice-home/practice-home.component";
import { PracticeHomeHeaderComponent } from "./components/practice-home-header/practice-home-header.component";
import { PracticePurposeComponent } from "./components/practice-purpose/practice-purpose.component";
import { PracticePrincipleCardComponent } from "./components/practice-principle-card/practice-principle-card.component";
import { PracticePathsComponent } from "./components/practice-paths/practice-paths.component";
import { PracticePathCardComponent } from "./components/practice-path-card/practice-path-card.component";
import { PracticeGuidanceComponent } from "./components/practice-guidance/practice-guidance.component";

@NgModule({
  imports: [CommonModule, PracticeRoutingModule],
  declarations: [
    PracticePage,
    PracticeGuidanceComponent,
    PracticePathCardComponent,
    PracticePathsComponent,
    PracticePrincipleCardComponent,
    PracticePurposeComponent,
    PracticeHomeHeaderComponent,
    PracticeHomeComponent
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class PracticeModule {}
