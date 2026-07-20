import { Component } from "@angular/core";
import { Router } from "@angular/router";

@Component({
  selector: "app-practice-home",
  templateUrl: "./practice-home.component.html",
  styleUrls: ["./practice-home.component.scss"],
  standalone: false
})
export class PracticeHomeComponent {
  constructor(private router: Router){}
  onNavigate(type: "general" | "topic") {
    this.router.navigate(["/practice/quizzes"])
  }
}
