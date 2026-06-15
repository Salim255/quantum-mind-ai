import { Component, Input } from "@angular/core";
import { NavItem } from "../../services/aside-nav.service";

@Component({
  selector: "app-aside-nav-link",
  templateUrl: "./aside-nav-link.component.html",
  styleUrl: "./aside-nav-link.component.scss",
  standalone: false
})
export class AsideNavLinkComponent {
  @Input() nav!: NavItem
}
