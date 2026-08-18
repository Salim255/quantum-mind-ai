import { Component, Input, signal } from "@angular/core";
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
    @Input() items!: NavItem| null

    currentPageNavSubscription!: Subscription;

    constructor(
      private router: Router,
      private asideNavService: AsideNavService
    ) {}

    ngOnInit(): void {
      this.listenToRouter()

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
