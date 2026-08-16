import { AfterViewInit, Component, computed, ElementRef, OnInit, QueryList, signal, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";
import { TopicWithSectionsDTO } from "../../interfaces/topic-with-sections.dto";
import { Subscription } from "rxjs";
import { LearnService } from "../../services/learn.service";


@Component({
  selector: "app-mathematics",
  templateUrl: "./mathematics.page.html",
  styleUrls: ["./mathematics.page.scss"],
  standalone: false
})
export class MathematicsPage implements OnInit, AfterViewInit {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;

  private mathsTopicsSubscription!: Subscription;

  mathsTopic = signal<TopicWithSectionsDTO | null>(null);

  mathBlocksSections = computed(() => {
      return {
        blocks: (this.mathsTopic()?.blocks ?? []).sort((a, b) => a.display_order - b.display_order),
        sections: (this.mathsTopic()?.sections ?? []).sort((a,b) => a.order_index - b.order_index),
      }
  });

  constructor(
    private learnService: LearnService,
    private pageAsideService: PageAsideService
  ){}

  ngOnInit(): void {
    this.subscribeToLearnTopics();
  }

  ngAfterViewInit(): void {
    this.observeSections();
  }

  subscribeToLearnTopics(){
    this.mathsTopicsSubscription = this.learnService.getTopicItem$(1)
    .subscribe((data: TopicWithSectionsDTO | null) => {
      this.mathsTopic.set(data);
    })
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
    this.mathsTopicsSubscription?.unsubscribe();
    this.observer?.disconnect();
  }
}
