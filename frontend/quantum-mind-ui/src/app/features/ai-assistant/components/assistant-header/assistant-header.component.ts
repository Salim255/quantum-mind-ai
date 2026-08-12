import { Component, output } from "@angular/core";

@Component({
  selector: "app-assistant-header",
  templateUrl: "./assistant-header.component.html",
  styleUrl: "./assistant-header.component.scss",
  standalone: false
})
export class AssistantHeaderComponent {

  protected readonly close = output<void>();

  protected onClose(): void {
    this.close.emit();
  }
}
