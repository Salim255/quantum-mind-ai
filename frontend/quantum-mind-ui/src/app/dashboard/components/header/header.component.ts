import { Component, CUSTOM_ELEMENTS_SCHEMA, signal } from "@angular/core";
import { MobileMenuComponent } from "../mobile-menu/mobile-menu.component";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { AsideNavService, NavItem } from "../../services/aside-nav.service";
import { filter, Subscription } from "rxjs";

@Component({
  selector: "app-header",
  templateUrl: "./header.component.html",
  styleUrl: "./header.component.scss",
  standalone: false,
})

export class HeaderComponent {

  protected readonly isMobileMenuOpen = signal(false);

  protected readonly mobileMenuConfig = {

  component: MobileMenuComponent,

  size: 'full' as const,

  showClose: false,

  closeOnBackdrop: true,

  closeOnEscape: true,
};

}
