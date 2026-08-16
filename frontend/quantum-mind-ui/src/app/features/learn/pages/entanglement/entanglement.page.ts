import { AfterViewInit, Component, computed, ElementRef, QueryList, signal, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";
import { TopicWithSectionsDTO } from "../../interfaces/topic-with-sections.dto";
import { LearnService } from "../../services/learn.service";
import { Subscription } from "rxjs";

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
  private entanglementTopicsSubscription!: Subscription;

  entanglementTopic  = signal<TopicWithSectionsDTO | null>(null);

  entanglementBlocksSections = computed(() => {
    return {
      blocks: (this.entanglementTopic()?.blocks ?? []).sort((a, b) => a.display_order - b.display_order),
      sections: (this.entanglementTopic()?.sections ?? []).sort((a,b) => a.order_index - b.order_index),
    }
  });

  constructor(
    private learnService: LearnService,
    private pageAsideService: PageAsideService,
  ){}

  ngOnInit(): void {
    this.subscribeToLearnTopics();
  }

  ngAfterViewInit(): void {
    this.observeSections();
  }

  subscribeToLearnTopics(){
    this.entanglementTopicsSubscription = this.learnService.getTopicItem$(3)
    .subscribe((data: TopicWithSectionsDTO | null) => {
      this.entanglementTopic.set(data);
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
    this.entanglementTopicsSubscription?.unsubscribe();
    this.observer?.disconnect();
  }
}
