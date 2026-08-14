import {
  ChangeDetectionStrategy,
  Component,
  computed,
  effect,
  input,
} from "@angular/core";

import { marked } from "marked";

declare const MathJax: {
  typesetPromise?: () => Promise<void>;
};

export type AssistantMessageRole =
  | "user"
  | "assistant";

export interface AssistantMessage {
  id: string;
  conversationId: string;
  role: AssistantMessageRole;
  isThinking?: boolean,
  content: string;
  createdAt: Date;
}

@Component({
  selector: "app-assistant-message",
  templateUrl: "./assistant-message.component.html",
  styleUrl: "./assistant-message.component.scss",
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: false,
})
export class AssistantMessageComponent {

  readonly message =
    input.required<AssistantMessage>();

  /**
   * Converts the assistant response from Markdown
   * into HTML.
   *
   * This computed value automatically recalculates
   * whenever message().content changes during
   * streaming.
   */
  protected readonly responseHtml =
    computed(() => {

      const message =
        this.message();

      if (message.role !== "assistant") {
        return "";
      }

      return marked.parse(
        message.content,
      ) as string;

    });


  /**
   * Animation frame used to coalesce multiple
   * MathJax requests during streaming.
   */
  private mathJaxFrameId:
    number | null = null;


  constructor() {

    effect(() => {

      /*
       * Establish the reactive dependency.
       *
       * When the assistant message changes,
       * this computed value is recalculated.
       */
      this.responseHtml();


      /*
       * Schedule MathJax after Angular has had
       * an opportunity to render the new HTML.
       */
      this.scheduleMathJax();

    });

  }


  /**
   * Schedule MathJax rendering.
   *
   * Streaming responses can update many times
   * per second. We don't want to execute MathJax
   * for every individual chunk.
   *
   * Multiple updates inside the same rendering
   * cycle are therefore collapsed into one
   * MathJax execution.
   */
  private scheduleMathJax(): void {

    if (
      this.mathJaxFrameId !== null
    ) {

      cancelAnimationFrame(
        this.mathJaxFrameId,
      );

    }


    this.mathJaxFrameId =
      requestAnimationFrame(() => {

        this.mathJaxFrameId = null;

        MathJax?.typesetPromise?.();

      });

  }


  /**
   * Cancel any pending animation frame when
   * the component is destroyed.
   */
  ngOnDestroy(): void {

    if (
      this.mathJaxFrameId !== null
    ) {

      cancelAnimationFrame(
        this.mathJaxFrameId,
      );

      this.mathJaxFrameId = null;

    }

  }

}
