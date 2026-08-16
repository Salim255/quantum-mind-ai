import { AfterViewInit, Component, computed, ElementRef, OnInit, QueryList, signal, ViewChildren } from "@angular/core";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";
import { Subscription } from "rxjs";
import { TopicWithSectionsDTO } from "../../interfaces/topic-with-sections.dto";
import { LearnService } from "../../services/learn.service";

@Component({
  selector: "app-spin-qubits",
  templateUrl: "./spin-qubits.page.html",
  styleUrls: ["./spin-qubits.page.scss"],
  standalone: false
})
export class SpinQubitsPage implements OnInit, AfterViewInit {
  @ViewChildren('pageSection')
  private sections!: QueryList<ElementRef<HTMLElement>>;
  private observer?: IntersectionObserver;

  private spinQuTopicsSubscription!: Subscription;

  spinQuTopic = signal<TopicWithSectionsDTO | null>(null);

  spinQuBlocksSections = computed(() => {
      return {
        blocks: (this.spinQuTopic()?.blocks ?? []).sort((a, b) => a.display_order - b.display_order),
        sections: (this.spinQuTopic()?.sections ?? []).sort((a,b) => a.order_index - b.order_index),
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
    this.spinQuTopicsSubscription = this.learnService.getTopicItem$(2)
    .subscribe((data: TopicWithSectionsDTO | null) => {
      this.spinQuTopic.set(data);
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
    this.spinQuTopicsSubscription?.unsubscribe();
    this.observer?.disconnect();
  }
}
