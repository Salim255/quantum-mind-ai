import { Component, Input } from "@angular/core";
import { NavItem } from "../../services/aside-nav.service";
import { ContentService } from "../../../features/learn/services/content.service";

@Component({
  selector: "app-primary-aside-nav-link",
  templateUrl: "./primary-aside-nav-link.component.html",
  styleUrl: "./primary-aside-nav-link.component.scss",
  standalone: false
})
export class PrimaryAsideNavLinkComponent {
  @Input() nav!: NavItem

  constructor(private contentService: ContentService){}

  onNavigate(nav: NavItem){
    if(nav?.sections) {
      this.contentService.setPageAsideContent(nav.sections);
    }
  }
}
