import { Component, ElementRef, QueryList, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";

@Component({
  selector: "app-classical-logic-page",
  templateUrl: "./classical-logic.page.html",
  styleUrl: "./classical-logic.page.scss",
  standalone: false
})
export class ClassicalLogicPage {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;

  constructor(private pageAsideService: PageAsideService){}

  ngOnInit(): void {
    //Called after the constructor, initializing input properties, and the first call to ngOnChanges.
    //Add 'implements OnInit' to the class.
    //this.observeSections();
  }

  ngAfterViewInit(): void {
      this.observeSections();
  }

  private observeSections(): void {

      this.observer = new IntersectionObserver(

          entries => {

              const visibleEntry = entries.find(
                  entry => entry.isIntersecting
              );

              if (!visibleEntry) {
                  return;
              }

              this.pageAsideService.setCurrentSectionId(
                  visibleEntry.target.id
              );

          },

          {
              root: null,

              threshold: 0.5
          }

      );

      this.sections.forEach(section => {
          this.observer!.observe(
              section.nativeElement
          );

      });
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
  }
}
