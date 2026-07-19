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
  private currentSectionIdSubscription!: Subscription;

  sections = signal<any []>([]);

  protected activeSection = signal<string>('');

  constructor(
    private pageAsideService: PageAsideService,
    private contentService: ContentService){}

  ngOnInit(): void {
    this.subscribeToPageAsideContent();
    this. subscribeToSectionId();
  }

  private subscribeToSectionId(){
    this.currentSectionIdSubscription = this.pageAsideService.getCurrentSectionId$.subscribe(
      id => {
        if(id) {
          this.activeSection.set(id);
        }
      }
    )
  }

  private subscribeToPageAsideContent(): void{
    this.pageAsideContentSubscription = this.contentService.getPageAsideContent$.subscribe(sections =>
      this.sections.set(sections)
    )
  }

  protected onNavigate(name: string){
     document
        .getElementById(name)
        ?.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
  }

  ngOnDestroy(): void {
    this.pageAsideContentSubscription?.unsubscribe();
    this.currentSectionIdSubscription?.unsubscribe();
  }
}
