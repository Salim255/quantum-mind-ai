import { AfterViewInit, Component, computed, ElementRef, OnDestroy, OnInit, QueryList, signal, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";
import { Subscription } from "rxjs";
import { TopicWithSectionsDTO } from "../../interfaces/topic-with-sections.dto";
import { LearnService } from "../../services/learn.service";

@Component({
  selector: "app-algorithms",
  templateUrl: "./quantum-impact.page.html",
  styleUrls: ["./quantum-impact.page.scss"],
  standalone: false
})
export class QuantumImpactPage implements AfterViewInit, OnInit, OnDestroy{
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;


  private quantumImpactTopicsSubscription!: Subscription;

  quantumImpactTopic = signal<TopicWithSectionsDTO | null>(null);

  quantumAImpactBlocksSections = computed(() => {
    return {
      blocks: (this.quantumImpactTopic()?.blocks ?? [])
        .sort((a, b) => a.display_order - b.display_order),
      sections: (this.quantumImpactTopic()?.sections ?? [])
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
    this.quantumImpactTopicsSubscription = this.learnService.getTopicItem$(8)
    .subscribe((data: TopicWithSectionsDTO | null) => {
      this.quantumImpactTopic.set(data);
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
    this.quantumImpactTopicsSubscription?.unsubscribe();
    this.observer?.disconnect();
  }
}
