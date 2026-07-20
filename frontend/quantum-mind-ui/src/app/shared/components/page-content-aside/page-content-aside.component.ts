import { Component, Input, OnInit, signal } from "@angular/core";
import { Subscription } from "rxjs";
import { ContentService } from "../../../features/learn/services/content.service";
import { PageAsideService } from "../../service/page-aside-content.service";


@Component({
  selector: "app-content-aside",
  templateUrl: "./page-content-aside.component.html",
  styleUrl: "./page-content-aside.component.scss",
  standalone: false
})
export class PageContentAsideComponent implements OnInit {
  @Input() scrollContainer!: HTMLElement;
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
    const container = document.querySelector('.learn-page__content') as HTMLElement | null;
    const target = document.getElementById(name);

    if (!container || !target) return;

    const top = target.offsetTop - container.offsetTop;
    console.log(top)
    container.scrollTo({
      top,
      behavior: 'smooth'
    });
  }

  ngOnDestroy(): void {
    this.pageAsideContentSubscription?.unsubscribe();
    this.currentSectionIdSubscription?.unsubscribe();
  }
}
