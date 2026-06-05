import { Component, signal } from "@angular/core";
import { AsideNavService, NavItem } from "../../services/aside-nav.service";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { filter, Subscription } from "rxjs";

@Component({
  selector: "app-aside-layout",
  templateUrl: "./aside-layout.component.html",
  styleUrls: ["./aside-layout.component.scss"],
  standalone: false
})

export class AsideLayoutComponent {
  items = signal<NavItem | null>(null)

  currentPageNavSubscription!: Subscription;

  constructor(
    private router: Router,
    private asideNavService: AsideNavService
  ) {

   }

  ngOnInit(): void {
    //Called after the constructor, initializing input properties, and the first call to ngOnChanges.
    //Add 'implements OnInit' to the class.
    console.log(this.router.url,"hello")

    console.log(this.items())

    this.listenToRouter()
  }

  listenToRouter(){
    console.log("Is runnign ")
     this.router.events
     .pipe(
    filter(event => event.type === EventType.NavigationEnd)
  ).
     subscribe((event: NavigationEnd) => {
        console.log('Router Event:', event);
        const url = event.url === '/' ? '/home' : this.router.url;
        this.asideNavService.setCurrentPageUrl(url)
    });
  }

  ngOnDestroy() {
    console.log('DESTROY');
  }
}
