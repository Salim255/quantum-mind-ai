import { Component, OnInit } from "@angular/core";
import { SidebarToggleService } from "../../dashboard/services/sidebar-toggle.service";

@Component({
  selector: "app-progress.page",
  templateUrl: "./progress.page.html",
  styleUrls: ["./progress.page.scss"],
  standalone: false
})

export class ProgressPage implements OnInit {
  /* Progress

  For tracking growth.

  Learning Progress
  Performance Analytics
  Strengths & Weaknesses
  Achievements
  Learning History
  Progress
  ├── Overview
  ├── Analytics
  ├── Achievements
  ├── Learning History
  └── Recommendations */

  constructor(
    private sidebarToggleService: SidebarToggleService
  ) {}

  ngOnInit(): void {
    // Initialize progress tracking logic here
    this.sidebarToggleService.setCollapsed(false); // Ensure sidebar is expanded for progress page
  }
}
