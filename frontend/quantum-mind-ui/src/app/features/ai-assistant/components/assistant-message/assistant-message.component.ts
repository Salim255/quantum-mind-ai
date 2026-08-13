import { ChangeDetectionStrategy, Component, input } from "@angular/core";

export type AssistantMessageRole =
  | "user"
  | "assistant";

export interface AssistantMessage {
  id: string;
  conversationId: string;
  role: AssistantMessageRole;
  content: string;
  createdAt: Date;
}

@Component({
  selector: "app-assistant-message",
  templateUrl: "./assistant-message.component.html",
  styleUrl: "./assistant-message.component.scss",
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: false
})
export class AssistantMessageComponent {

  readonly message = input.required<AssistantMessage>();

}
