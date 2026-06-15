import { Component, Input, OnInit, signal } from "@angular/core";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { filter } from "rxjs";
import { ContentService } from "../../../features/learn/services/content.service";

@Component({
  selector: "app-content-aside",
  templateUrl: "./page-content-aside.component.html",
  styleUrl: "./page-content-aside.component.scss",
  standalone: false
})
export class PageContentAsideComponent implements OnInit {
  list = signal<any []>([])

  constructor(
    private contentService: ContentService,
    private router: Router
  ){}
  ngOnInit(): void {
    this.listenToRouter()
  }

  listenToRouter(): void {
     this.router.events.pipe(
        filter(event => event.type === EventType.NavigationEnd)
      ).subscribe((event: NavigationEnd) => {
          const url = event.url === '/' ? '/home' : this.router.url;
          console.log(url);
          this.list.set(this.contentService.getAsideContent()) ;
      });
  }

}
