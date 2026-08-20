import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { PracticePage } from "./practice.page";
import { PracticeRoutingModule } from "./practice-routing.module";
import { PracticeHomeComponent } from "./components/practice-home/practice-home.component";
import { PracticeHomeHeaderComponent } from "./components/practice-home-header/practice-home-header.component";
import { PracticePurposeComponent } from "./components/practice-purpose/practice-purpose.component";

@NgModule({
  imports: [CommonModule, PracticeRoutingModule],
  declarations: [
    PracticePage,
    PracticePurposeComponent,
    PracticeHomeHeaderComponent,
    PracticeHomeComponent
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class PracticeModule {}
