import { Component, Input, OnChanges } from "@angular/core";
import * as katex from "katex";

@Component({
  selector: "app-circuits",
  template: `
  <div [innerHTML]="html"></div>`,
  standalone: false
})
export class CircuitsComponent implements OnChanges {
  @Input() latex = '';

  html = '';

  ngOnChanges(): void {
    this.html = katex.renderToString(this.latex, {
      throwOnError: false,
      displayMode: true
    });
  }
}
