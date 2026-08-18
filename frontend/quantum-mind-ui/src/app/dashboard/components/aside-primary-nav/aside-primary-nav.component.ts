import { Component, Input, signal } from "@angular/core";
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
  @Input() items!: NavItem| null

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

}
