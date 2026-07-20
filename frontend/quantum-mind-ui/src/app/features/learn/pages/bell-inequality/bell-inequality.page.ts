import { Component, ElementRef, QueryList, ViewChildren } from "@angular/core";

@Component({
  selector: "app-bell-inequality-page",
  templateUrl: "./bell-inequality.page.html",
  styleUrl: "./bell-inequality.page.scss",
  standalone: false
})
export class BellInequalityPage {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;
}
