import { Injectable } from "@angular/core";
import { NAVIGATION } from "./data";
import { BehaviorSubject, Observable } from "rxjs";
import { BreadcrumbService } from "./bread-crumbs.service";

export interface NavItem {
  name: string;
  path: string;
  icon?: string;
  description?: string;
  children?: NavItem[];
}


@Injectable({providedIn: "root"})
export class AsideNavService {
  private currentPageUrlSubject = new BehaviorSubject<NavItem | null >(null)

  constructor(private breadcrumbService: BreadcrumbService){}

  setCurrentPageUrl(url: string){
    const pageNavs: NavItem | null = this.getAsideNav(url) ?? null;

    this.currentPageUrlSubject.next(pageNavs);
    // Bread crumbs
    this.breadcrumbService.setAppBreadCrumbs(url);
  }

  get getCurrentPageNav$():Observable<NavItem | null> {
    return this.currentPageUrlSubject.asObservable()
  }

  private getAsideNav(currentRoute: string): NavItem | undefined {
    return NAVIGATION.find(item =>
      currentRoute.startsWith(item.path)
    );
  }
}
