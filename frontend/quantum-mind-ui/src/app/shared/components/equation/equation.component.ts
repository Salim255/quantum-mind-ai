import { Component, Input, OnChanges, signal } from "@angular/core";
import * as katex from "katex";

@Component({
  selector: "app-equation",
  templateUrl: "./equation.component.html",
  standalone: false
})
export class EquationComponent implements OnChanges {
  @Input() latex = '';
  html = signal("");

   ngOnChanges(): void {
      const equation = katex.renderToString(this.latex, {
        throwOnError: false,
        displayMode: true
      });

      this.html.set(equation)
    }

}
