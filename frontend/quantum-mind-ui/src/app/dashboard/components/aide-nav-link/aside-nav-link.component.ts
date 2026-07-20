import { Component, Input } from "@angular/core";
import { NavItem } from "../../services/aside-nav.service";
import { ContentService } from "../../../features/learn/services/content.service";

@Component({
  selector: "app-aside-nav-link",
  templateUrl: "./aside-nav-link.component.html",
  styleUrl: "./aside-nav-link.component.scss",
  standalone: false
})
export class AsideNavLinkComponent {
  @Input() nav!: NavItem

  constructor(private contentService: ContentService){}

  onNavigate(nav: NavItem){
    if(nav?.sections) {
      this.contentService.setPageAsideContent(nav.sections);
    }
  }
}
