import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { OverviewRoutingModule } from "./overview-routing.module";
import { OverviewPage } from "./overview.page";

@NgModule({
  imports: [
    CommonModule,
    OverviewRoutingModule
  ],
  declarations: [OverviewPage],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class OverviewModule {}
