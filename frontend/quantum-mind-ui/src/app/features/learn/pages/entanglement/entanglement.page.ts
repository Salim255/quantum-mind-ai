import { AfterViewInit, Component, ElementRef, QueryList, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";

@Component({
  selector: "app-entanglement-page",
  templateUrl: "./entanglement.page.html",
  styleUrl: "./entanglement.page.scss",
  standalone: false
})
export class EntanglementPage implements AfterViewInit {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;

  constructor(private pageAsideService: PageAsideService){}

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
              rootMargin: "-80px 0px -60% 0px",
              threshold: 0
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
