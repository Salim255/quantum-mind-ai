import { Injectable } from "@angular/core";
import { NAVIGATION } from "./data";
import { NavigationEnd, Router } from "@angular/router";
import { BehaviorSubject, filter, Observable } from "rxjs";

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

  setCurrentPageUrl(url: string){
    const pageNavs: NavItem | null = this.getAsideNav(url) ?? null;
    this.currentPageUrlSubject.next(pageNavs);
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
