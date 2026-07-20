import { AfterViewInit, Component, ElementRef, OnInit, QueryList, signal, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";


@Component({
  selector: "app-mathematics",
  templateUrl: "./mathematics.page.html",
  styleUrls: ["./mathematics.page.scss"],
  standalone: false
})
export class MathematicsPage implements AfterViewInit {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;
  htmlSections = signal<any[]>([]);

  constructor(private pageAsideService: PageAsideService){}

  ngAfterViewInit(): void {
    this.observeSections();
  }

  equation =
    'H|0\\rangle = \\frac{1}{\\sqrt{2}} (|0\\rangle + |1\\rangle)';

    qubitVector = String.raw`
      \begin{bmatrix}
      \alpha \\
      \beta
      \end{bmatrix}
      `;
   polynomial = String.raw`x^2 + 4x + 4 = 0`;

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

      this.sections?.forEach(section => {
        this.observer!.observe(
          section.nativeElement
        );
      });
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
  }
}
