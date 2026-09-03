import { CommonModule } from "@angular/common";
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from "@angular/core";
import { ExplorePage } from "./explore.page";
import { ExploreRoutingModule } from "./explore-routing.module";
import { ExploreTopicComponent } from "./components/explore-topic/explore-topic.component";
import { ExploreHeaderComponent } from "./components/explore-header/explore-header.component";

@NgModule({
  imports: [CommonModule, ExploreRoutingModule],
  declarations: [
    ExploreHeaderComponent,
    ExploreTopicComponent,
    ExplorePage
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})

export class ExploreModule {}
