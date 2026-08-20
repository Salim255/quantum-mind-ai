import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { ExplorePage } from "./explore.page";
import { ExploreRoutingModule } from "./explore-routing.module";

@NgModule({
  imports: [CommonModule, ExploreRoutingModule],
  declarations: [ExplorePage],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class ExploreModule {}
