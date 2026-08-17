import { Component, signal } from "@angular/core";
import { AsideNavService, NavItem } from "../../services/aside-nav.service";
import { filter, Subscription } from "rxjs";
import { EventType, NavigationEnd, Router } from "@angular/router";

@Component({
  selector: "app-aside-secondary-nav",
  templateUrl: "./aside-secondary-nav.component.html",
  styleUrl: "./aside-secondary-nav.component.scss",
  standalone: false
})
export class AsideSecondaryNavComponent {
  items = signal<NavItem| null>(null)

    currentPageNavSubscription!: Subscription;

    constructor(
      private router: Router,
      private asideNavService: AsideNavService
    ) {}

    ngOnInit(): void {
      this.listenToRouter()
      this.subscribeToCurrentPageNav()
    }

    subscribeToCurrentPageNav(): void{
      this.currentPageNavSubscription = this.asideNavService
      .getCurrentPageNav$.subscribe((value: NavItem | null) => {
        if(!value) {
          const url = this.router.url === '/' ? '/home' : this.router.url;
          this.asideNavService.setCurrentPageUrl(url);
          return
        }
        this.items.set(value);
      })
    }

    listenToRouter(): void {
       this.router.events.pipe(
          filter(event => event.type === EventType.NavigationEnd)
        ).subscribe((event: NavigationEnd) => {
            const url = event.url === '/' ? '/home' : this.router.url;

            this.asideNavService.setCurrentPageUrl(url)
        });
    }

    ngOnDestroy() {
      this.currentPageNavSubscription?.unsubscribe()
    }
}
