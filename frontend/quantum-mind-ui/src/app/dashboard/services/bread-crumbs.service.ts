import { Injectable } from "@angular/core";
import { NAVIGATION } from "./data";

export interface Breadcrumb {
  name: string;
  path: string;
}

@Injectable({providedIn: 'root'})
export class BreadcrumbService {
  constructor(){}

  buildBreadcrumbs(url: string): Breadcrumb[] {
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
