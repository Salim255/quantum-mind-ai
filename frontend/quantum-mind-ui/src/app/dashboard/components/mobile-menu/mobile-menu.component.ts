import { Component, signal } from "@angular/core";
import { AsideNavService, NavItem } from "../../services/aside-nav.service";
import { Subscription } from "rxjs";
import { ContentService } from "../../../features/learn/services/content.service";
import { MobileMenuService } from "../../services/mobile-menu.service";

@Component({
  selector: "app-mobile-menu",
  templateUrl: "./mobile-menu.component.html",
  styleUrl: "./mobile-menu.component.scss",
  standalone: false
})
export class MobileMenuComponent {
  items = signal<NavItem | null>(null)

  currentPageNavSubscription!: Subscription;


  constructor(
    private mobileMenuService: MobileMenuService,
    private contentService: ContentService,
    private asideNavService: AsideNavService
  ) {}

  ngOnInit(): void {
    this.subscribeToCurrentPageNav()
  }

  onNavigate(nav: NavItem){
    if(nav?.sections) {
      this.contentService.setPageAsideContent(nav.sections);
    }
    
    this.mobileMenuService.close();
  }

  subscribeToCurrentPageNav(): void{
    this.currentPageNavSubscription = this.asideNavService
    .getCurrentPageNav$.subscribe((value: NavItem | null) => {
      this.items.set(value);
    })
  }


  ngOnDestroy() {
    this.currentPageNavSubscription?.unsubscribe()
  }
}
