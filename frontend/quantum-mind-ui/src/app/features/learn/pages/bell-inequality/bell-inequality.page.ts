import { AfterViewInit, Component, computed, ElementRef, OnInit, QueryList, signal, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";
import { TopicWithSectionsDTO } from "../../interfaces/topic-with-sections.dto";
import { LearnService } from "../../services/learn.service";
import { Subscription } from "rxjs";

@Component({
  selector: "app-bell-inequality-page",
  templateUrl: "./bell-inequality.page.html",
  styleUrl: "./bell-inequality.page.scss",
  standalone: false
})
export class BellInequalityPage implements OnInit, AfterViewInit {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;
  private bellTopicsSubscription!: Subscription;

  bellTopic = signal<TopicWithSectionsDTO | null>(null);

  bellBlocksSections = computed(() => {
    return {
      blocks: (this.bellTopic()?.blocks ?? []).sort((a, b) => a.display_order - b.display_order),
      sections: (this.bellTopic()?.sections ?? []).sort((a,b) => a.order_index - b.order_index),
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
    this.bellTopicsSubscription = this.learnService.getTopicItem$(4)
    .subscribe((data: TopicWithSectionsDTO | null) => {
      this.bellTopic.set(data);
    })
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

      this.sections?.forEach(section => {
        this.observer!.observe(
          section.nativeElement
        );
      });
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
    this.bellTopicsSubscription?.unsubscribe();
  }
}
