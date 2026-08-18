import { Component, HostListener, Input, signal } from "@angular/core";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { filter, Subscription } from "rxjs";
import { AsideNavService, NavItem } from "../../services/aside-nav.service";

@Component({
  selector: "app-aside-primary-nav",
  templateUrl: "./aside-primary-nav.component.html",
  styleUrl: "./aside-primary-nav.component.scss",
  standalone: false
})
export class AsidePrimaryNavComponent {
  items = signal< NavItem| null>(null);

  isExpanded = signal<boolean>(false);

  constructor(private asideNavService: AsideNavService) {}

  ngOnInit(): void {
    this.items.set(this.asideNavService.getPrimaryNavData());
  }


  @HostListener('mouseenter')
  onMouseEnter(): void {

    this.isExpanded.set(true);

  }


  @HostListener('mouseleave')
  onMouseLeave(): void {

    this.isExpanded.set(false);

  }

}
