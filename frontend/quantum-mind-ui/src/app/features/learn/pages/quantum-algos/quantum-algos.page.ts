import { AfterViewInit, Component, computed, ElementRef, OnDestroy, OnInit, QueryList, signal, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";
import { TopicWithSectionsDTO } from "../../interfaces/topic-with-sections.dto";
import { LearnService } from "../../services/learn.service";
import { Subscription } from "rxjs";

@Component({
  selector: "app-quantum-algos-page",
  templateUrl: "./quantum-algos.page.html",
  styleUrl: "./quantum-algos.page.scss",
  standalone: false
})
export class QuantumAlgosPage implements OnInit, AfterViewInit, OnDestroy {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;


  private quantumAlgosTopicsSubscription!: Subscription;

  quantumAlgosTopic = signal<TopicWithSectionsDTO | null>(null);

  quantumAlgosBlocksSections = computed(() => {
    return {
      blocks: (this.quantumAlgosTopic()?.blocks ?? [])
        .sort((a, b) => a.display_order - b.display_order),
      sections: (this.quantumAlgosTopic()?.sections ?? [])
        .sort((a,b) => a.order_index - b.order_index),
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
    this.quantumAlgosTopicsSubscription = this.learnService.getTopicItem$(7)
    .subscribe((data: TopicWithSectionsDTO | null) => {
      this.quantumAlgosTopic.set(data);
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
    this.quantumAlgosTopicsSubscription?.unsubscribe();
    this.observer?.disconnect();
  }
}
