import { Component, OnDestroy, OnInit, signal } from "@angular/core";
import { LearnService } from "../features/learn/services/learn.service";
import { AIAssistantService } from "../features/ai-assistant/service/ai-assistant.service";
import { Subscription } from "rxjs";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.page.html",
  styleUrls: ["./dashboard.page.scss"],
  standalone:false
})
export class DashboardPage implements OnInit, OnDestroy {
  private isAssistantVisibleSubscription!: Subscription;

  closeAside = signal<boolean>(JSON.parse(localStorage.getItem("asideIsClose") ?? 'true'));

  isAssistantVisible = signal<boolean>(false);

  assistantWidth = signal<number>(420)

  constructor(
    private aiAssistantService: AIAssistantService,
    private learnService: LearnService
  ) {}


  ngOnInit(): void {
    this.learnService.getTopics().subscribe();

    this.subscribeToIsAssistantVisible();
  }


  private subscribeToIsAssistantVisible(){
    this.isAssistantVisibleSubscription = this.aiAssistantService.isAssistantVisible$.subscribe(
      value => this.isAssistantVisible.set(value)
    )
  }

  ngOnDestroy(): void {
    this.isAssistantVisibleSubscription?.unsubscribe();
  }
}
