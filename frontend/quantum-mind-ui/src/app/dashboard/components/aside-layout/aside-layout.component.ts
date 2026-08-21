import { Component, signal } from "@angular/core";
import { AsideNavService, NavItem } from "../../services/aside-nav.service";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { filter, Subscription } from "rxjs";
import { SidebarToggleService } from "../../services/sidebar-toggle.service";

@Component({
  selector: "app-aside-layout",
  templateUrl: "./aside-layout.component.html",
  styleUrls: ["./aside-layout.component.scss"],
  standalone: false
})

export class AsideLayoutComponent {
  items = signal<NavItem | null>(null)

  private currentPageNavSubscription!: Subscription;
  private sidebarToggleSubscription!: Subscription;
  showSecondaryNav = signal<boolean>(false);
  
  constructor(
    private sidebarToggleService: SidebarToggleService,
    private router: Router,
    private asideNavService: AsideNavService
  ) {}

  ngOnInit(): void {
    this.listenToRouter()
    this.subscribeToCurrentPageNav();
    this.subscribeToSidebarToggle();
  }

  subscribeToSidebarToggle(){
    this.sidebarToggleSubscription = this.sidebarToggleService
    .collapsed$.subscribe(stat => {
      this.showSecondaryNav.set(stat);
    })
  }

  subscribeToCurrentPageNav(): void{
    this.currentPageNavSubscription = this.asideNavService
    .getCurrentPageNav$.subscribe((value: NavItem | null) => {
      if(!value) {
        const url = this.router.url === '/' ? '/home' : this.router.url;
        this.asideNavService.setCurrentPageUrl(url);

        this.setHideSecondaryStatus(url);

        return
      }
      this.items.set(value);
    })
  }

  private setHideSecondaryStatus(url: string): void {
    const hasSecond =  [
      '/learn',
      '/quizzes',
      ,
    ].some(route =>
      url === route ||
      url.startsWith(`${route}/`)
    );

    this.showSecondaryNav.set(hasSecond);
  }

  

  listenToRouter(): void {
     this.router.events.pipe(
        filter(event => event.type === EventType.NavigationEnd)
      ).subscribe((event: NavigationEnd) => {
          const url = event.url == '/' ? '/home' : this.router.url;

          this.setHideSecondaryStatus(url);

          this.asideNavService.setCurrentPageUrl(url)
      });
  }

  ngOnDestroy() {
     this.sidebarToggleSubscription?.unsubscribe();
    this.currentPageNavSubscription?.unsubscribe()
  }
}
