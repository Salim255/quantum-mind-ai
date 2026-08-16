import {
  ChangeDetectionStrategy,
  Component,
  input,
} from "@angular/core";

@Component({
  selector: "app-split-panel",
  templateUrl: "./split-panel.component.html",
  styleUrl: "./split-panel.component.scss",
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: false,
})
export class SplitPanelComponent {

  /**
   * Percentage size of each split area.
   *
   * Example:
   * [60, 40]
   */
  readonly sizes = input<number[]>([60, 40]);


  /**
   * Minimum size of each split area.
   *
   * Example:
   * [0, 40]
   */
  readonly minSizes = input<number[]>([0, 0]);


  /**
   * Maximum size of each split area.
   *
   * Example:
   * [60, 100]
   */
  readonly maxSizes = input<number[]>([100, 100]);


  /**
   * Size of the draggable gutter.
   */
  readonly gutterSize = input<number>(2);


  /**
   * Split direction.
   *
   * horizontal:
   * ┌──────┬──────┐
   *
   * vertical:
   * ┌─────────────┐
   * ├─────────────┤
   */
  readonly direction =
    input<"horizontal" | "vertical">("horizontal");

}
