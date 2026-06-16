import { Component } from "@angular/core";
import { Subscription } from "rxjs";
import { PageAsideService } from "../../../../shared/service/page-aside-content.service";

@Component({
  selector: "app-spin-page",
  templateUrl: "./spin.page.html",
  styleUrl: "./spin.page.scss",
  standalone: false
})
export class SpinPage {
  constructor(private pageAsideService: PageAsideService){}
}
