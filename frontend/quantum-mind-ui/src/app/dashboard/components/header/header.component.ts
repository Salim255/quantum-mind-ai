import { Component, CUSTOM_ELEMENTS_SCHEMA, OnDestroy, OnInit, signal } from "@angular/core";
import { MobileMenuComponent } from "../mobile-menu/mobile-menu.component";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { AsideNavService, NavItem } from "../../services/aside-nav.service";
import { filter, Subscription } from "rxjs";
import { MobileMenuService } from "../../services/mobile-menu.service";
import { ModalVariant } from "../../../shared/kits/modal/modal-config";

@Component({
  selector: "app-header",
  templateUrl: "./header.component.html",
  styleUrl: "./header.component.scss",
  standalone: false,
})

export class HeaderComponent implements OnInit, OnDestroy {
  private isMobileMenuOpenSubscription!: Subscription;

  isMobileMenuOpen = signal(false);

  protected readonly mobileMenuConfig = {

    component: MobileMenuComponent,

    variant: 'menu' as ModalVariant,

    size: 'full' as const,

    title: 'Quantum Mind',

    showClose: true,

    closeOnBackdrop: true,

    closeOnEscape: true,

    onClose: () => {
      this.mobileMenuService.close();
    },
  };

  constructor(private mobileMenuService: MobileMenuService){}

  ngOnInit(): void {
    this.subscribeToMobileMenu(); 
  }

  onMobileMenu(){
    this.mobileMenuService.toggle();
  }

  private subscribeToMobileMenu(){
    this.isMobileMenuOpenSubscription = this.mobileMenuService.isOpen$.subscribe(stat => {
        this.isMobileMenuOpen.set(stat);
    });
  }

  ngOnDestroy(): void {
    this.isMobileMenuOpenSubscription?.unsubscribe();
  }

}
