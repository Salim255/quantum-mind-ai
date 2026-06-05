import { Injectable } from "@angular/core";

export interface Breadcrumb {
  name: string;
  path: string;
}

@Injectable({providedIn: 'root'})
export class BreadcrumbService {
  constructor(){}
}
