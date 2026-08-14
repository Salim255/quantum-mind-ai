import {
  ChangeDetectionStrategy,
  Component,
} from "@angular/core";

@Component({
  selector: "app-assistant-error",
  templateUrl: "./assistant-error.component.html",
  styleUrl: "./assistant-error.component.scss",
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: false,
})
export class AssistantErrorComponent {}
