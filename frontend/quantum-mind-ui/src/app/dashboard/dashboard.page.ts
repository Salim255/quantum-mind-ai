import { Component, signal } from "@angular/core";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.page.html",
  styleUrls: ["./dashboard.page.scss"],
  standalone:false
})
export class DashboardPage {

  closeAside = signal<boolean>(JSON.parse(localStorage.getItem("asideIsClose") ?? 'true'));
  constructor() {}

 /*  Minimal v1 Navigation

  For your current stage, I'd keep it lean:

  Dashboard
  Topics
  Learning Paths
  Quizzes
  Assessments
  Progress
  Resources
  Example Dashboard Cards

  When users land on the dashboard:

  Continue Learning
  Recommended Topics
  Recent Quiz Results
  Progress Overview
  Knowledge Score
  Upcoming Challenges

  For a professional learning platform, my favorite structure would be:

  Dashboard
  Learn
  Practice
  Assess
  Progress
  Resources

  It's simple, scalable, and mirrors how people naturally learn: */
}
