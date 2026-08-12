import { Component, OnInit, signal } from "@angular/core";
import { LearnService } from "../features/learn/services/learn.service";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.page.html",
  styleUrls: ["./dashboard.page.scss"],
  standalone:false
})
export class DashboardPage implements OnInit {

  closeAside = signal<boolean>(JSON.parse(localStorage.getItem("asideIsClose") ?? 'true'));
  assistantWidth = signal<number>(420)
  constructor(private learnService: LearnService) {}


  ngOnInit(): void {
    this.learnService.getTopics().subscribe()
  }


}
