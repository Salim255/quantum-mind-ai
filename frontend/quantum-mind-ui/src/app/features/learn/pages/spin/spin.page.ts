import { AfterViewInit, Component, computed, ElementRef, OnDestroy, OnInit, QueryList, signal, ViewChildren } from "@angular/core";
import { Subscription } from "rxjs";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";
import { LearnService } from "../../services/learn.service";
import { TopicWithSectionsDTO } from "../../interfaces/topic-with-sections.dto";

@Component({
  selector: "app-spin-page",
  templateUrl: "./spin.page.html",
  styleUrl: "./spin.page.scss",
  standalone: false
})
export class SpinPage  implements AfterViewInit, OnInit, OnDestroy {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;

  private spinTopicsSubscription!: Subscription;

  spanTopic = signal<TopicWithSectionsDTO | null>(null);

  topicBlocks = computed(() => {
    return [
      ...(this.spanTopic()?.blocks.sort((a, b) => a.display_order - b.display_order)) ?? []
    ]
  })

  sectionsList = computed(( ) => {
    return [
      ...(
        this.spanTopic()?.sections?.sort((a, b) => a.order_index - b.order_index))
        ?.map(section => ({
          ...section,
          blocks: section.blocks.sort((a, b) => a.display_order - b.display_order)
        })) ?? []
    ]
  })

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
    this.spinTopicsSubscription = this.learnService.getTopicItem$(0)
    .subscribe((data: TopicWithSectionsDTO | null) => {
      this.spanTopic.set(data);
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
    this.spinTopicsSubscription?.unsubscribe();
    this.observer?.disconnect();
  }
}
