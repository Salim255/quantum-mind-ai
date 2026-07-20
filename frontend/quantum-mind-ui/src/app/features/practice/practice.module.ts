import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { PracticePage } from "./practice.page";
import { PracticeRoutingModule } from "./practice-routing.module";
import { PracticeHomeComponent } from "./components/practice-home/practice-home.component";

@NgModule({
  imports: [CommonModule, PracticeRoutingModule],
  declarations: [PracticePage, PracticeHomeComponent],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class PracticeModule {}
