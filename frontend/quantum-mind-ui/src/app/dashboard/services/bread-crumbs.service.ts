import { Injectable } from "@angular/core";
import { NAVIGATION } from "./data";
import { BehaviorSubject, Observable } from "rxjs";

export interface Breadcrumb {
  name: string;
  path: string;
}

@Injectable({providedIn: 'root'})
export class BreadcrumbService {
  private appBreadCrumbSubject = new BehaviorSubject< Breadcrumb[]>([]);

  constructor(){}

  setAppBreadCrumbs(url: string){
    const breadcrumb: Breadcrumb[] = this.buildBreadcrumbs(url);
    console.log(breadcrumb);
    this.appBreadCrumbSubject.next(breadcrumb);
  }

  get getAppBreadCrumbs$(): Observable<Breadcrumb[]>{
    return this.appBreadCrumbSubject.asObservable();
  }

  private buildBreadcrumbs(url: string): Breadcrumb[] {
    const breadcrumbs: Breadcrumb[] = [
      {
        name: 'Home',
        path: '/home'
      }
    ];

    for (const section of NAVIGATION) {

      // Skip home because we already added it
      if (section.path === '/home') {
        continue;
      }

      // Match section itself
      if (url === section.path) {
        breadcrumbs.push({
          name: section.name,
          path: section.path
        });

        return breadcrumbs;
      }

      // Match child page
      const child = section.children?.find(
        child => child.path === url
      );

      if (child) {
        breadcrumbs.push({
          name: section.name,
          path: section.path
        });

        breadcrumbs.push({
          name: child.name,
          path: child.path
        });

        return breadcrumbs;
      }
    }

    return breadcrumbs;
  }
}
