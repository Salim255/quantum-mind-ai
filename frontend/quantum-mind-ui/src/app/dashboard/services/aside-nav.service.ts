import { Injectable } from "@angular/core";

export interface LinkItem {
  path: string;
  name: string
}
export const Nav_Data = {
  learn: {
    links: [
      {
        path: "",
        name: ""
      }
    ]
  },
  home: {},
  explore: {},
  practice: {},
  progress: {},
  resources: {}
}
export enum PageName {
  LEARN="learn",
  HOME="home",
  EXPLORE="explore",
  PRACTICE="practice",
  PROGRESS="progress"
}

@Injectable({providedIn: "root"})
export class AsideNavService {

  built_links_by_page(page: PageName){

  }
}
