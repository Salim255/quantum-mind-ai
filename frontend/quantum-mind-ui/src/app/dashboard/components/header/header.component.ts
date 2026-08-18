import { Component, signal } from "@angular/core";
import { MobileMenuComponent } from "../mobile-menu/mobile-menu.component";


@Component({
  selector: "app-header",
  templateUrl: "./header.component.html",
  styleUrl: "./header.component.scss",
  standalone: false,
})

export class HeaderComponent {

  protected readonly isMobileMenuOpen = signal(true);

  protected readonly mobileMenuConfig = {

  component: MobileMenuComponent,

  size: 'full' as const,

  showClose: false,

  closeOnBackdrop: true,

  closeOnEscape: true,
};

}
