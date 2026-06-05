import { Component, OnDestroy, OnInit, signal } from "@angular/core";
import { Breadcrumb, BreadcrumbService } from "../../services/bread-crumbs.service";
import { Subscription } from "rxjs";

@Component({
  selector: "app-bread-crumbs",
  templateUrl: "./bread-crumbs.component.html",
  styleUrls: ["./bread-crumbs.component.scss"],
  standalone: false
})
export class BreadCrumbsComponent implements OnInit, OnDestroy {
  private breadCrumbsSubscription!: Subscription;
  breadcrumbs = signal<Breadcrumb[]>([]);

  constructor(private breadcrumbService: BreadcrumbService){}

  ngOnInit(): void {
    this.subscribeToBreadCrumbs();
  }

  normalizeUrl(path: string ): string{
    return path === '/home' ? '/' : path;
  }

  subscribeToBreadCrumbs(){
    this.breadCrumbsSubscription = this.breadcrumbService.getAppBreadCrumbs$
    .subscribe((value: Breadcrumb[]) => {
        console.log(value)
        this.breadcrumbs.set(value)
    })
  }
  ngOnDestroy(): void {
    this.breadCrumbsSubscription?.unsubscribe();
  }
}
