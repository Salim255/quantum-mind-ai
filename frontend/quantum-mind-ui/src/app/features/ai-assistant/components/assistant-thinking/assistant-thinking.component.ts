import {
  ChangeDetectionStrategy,
  Component,
} from "@angular/core";

@Component({
  selector: "app-assistant-thinking",
  templateUrl: "./assistant-thinking.component.html",
  styleUrl: "./assistant-thinking.component.scss",
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: false,
})
export class AssistantThinkingComponent {}
