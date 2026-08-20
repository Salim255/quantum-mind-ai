import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { ExplorePage } from "./explore.page";
import { ExploreRoutingModule } from "./explore-routing.module";

@NgModule({
  imports: [CommonModule, ExploreRoutingModule],
  declarations: [ExplorePage]
})

export class ExploreModule {}
