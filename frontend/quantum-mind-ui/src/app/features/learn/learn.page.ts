import { Component, OnDestroy, OnInit, signal } from "@angular/core";
import { ContentService } from "./services/content.service";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { filter, Subscription } from "rxjs";
import { LearnService } from "./services/learn.service";

@Component({
  selector: "app-learn-page",
  templateUrl: "./learn.page.html",
  styleUrls: ["./learn.page.scss"],
  standalone: false
})
export class LearnPage implements OnInit, OnDestroy{
  closeAside = signal<boolean>(JSON.parse(localStorage.getItem("asideIsClose") ?? 'false'));
  private currentSectionIdSubscription!: Subscription;
  private learnTopicsSubscription!: Subscription;

  constructor(
    private learnService: LearnService,
    private router: Router,
    private contentService: ContentService
  ){}

  ngOnInit(): void {
    this.listenToRouter();
  }



  listenToRouter(): void {
     this.router.events.pipe(
        filter(event => event.type === EventType.NavigationEnd)
      ).subscribe((event: NavigationEnd) => {
          const url =  event.url;
          
          this.closeAside.set(url.startsWith('/learn/'));
          localStorage.setItem("asideIsClose", JSON.stringify(this.closeAside()));
    
      });
  }

  ngOnDestroy(): void {

    console.log("destroy")
    this.contentService.clearStorage();
    this.currentSectionIdSubscription?.unsubscribe();
    this.learnTopicsSubscription?.unsubscribe();

  }
}
