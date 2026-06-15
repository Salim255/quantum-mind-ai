import { Component, Input, OnInit, signal } from "@angular/core";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { filter, Subscription } from "rxjs";
import { ContentService } from "../../../features/learn/services/content.service";

@Component({
  selector: "app-content-aside",
  templateUrl: "./page-content-aside.component.html",
  styleUrl: "./page-content-aside.component.scss",
  standalone: false
})
export class PageContentAsideComponent implements OnInit {
  private pageAsideContentSubscription!: Subscription;
  sections = signal<any []>([])

  constructor(private contentService: ContentService){}

  ngOnInit(): void {
    this.subscribeToPageAsideContent();
  }

  subscribeToPageAsideContent(): void{
    this.pageAsideContentSubscription = this.contentService.getPageAsideContent$.subscribe(sections =>
      this.sections.set(sections)
    )
  }

  ngOnDestroy(): void {
    this.pageAsideContentSubscription?.unsubscribe();
  }
}
