import { Component, OnInit, signal } from "@angular/core";
import { Subscription, take } from "rxjs";
import { ContentService } from "../../../features/learn/services/content.service";
import { NgZone } from '@angular/core';
import { PageAsideService } from "../../service/page-aside-content.service";


@Component({
  selector: "app-content-aside",
  templateUrl: "./page-content-aside.component.html",
  styleUrl: "./page-content-aside.component.scss",
  standalone: false
})
export class PageContentAsideComponent implements OnInit {
  private pageAsideContentSubscription!: Subscription;
  sections = signal<any []>([])


  constructor(
    private pageAsideService: PageAsideService,
    private contentService: ContentService){}

  ngOnInit(): void {
    this.subscribeToPageAsideContent();
  }

  subscribeToPageAsideContent(): void{
    this.pageAsideContentSubscription = this.contentService.getPageAsideContent$.subscribe(sections =>
      this.sections.set(sections)
    )
  }

  onNavigate(id: string){
    console.log(id)
    this.pageAsideService.setCurrentId(id);
  }

  ngOnDestroy(): void {
    this.pageAsideContentSubscription?.unsubscribe();
  }
}
