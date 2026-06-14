import { Component, Input, OnChanges, signal } from "@angular/core";
import * as katex from "katex";
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: "app-equation",
  templateUrl: "./equation.component.html",
  standalone: false
})
export class EquationComponent implements OnChanges {
  @Input() latex = '';
  html!: SafeHtml;

  constructor(private sanitizer: DomSanitizer){}

  ngOnChanges(): void {
    const equation = katex.renderToString(this.latex, {
      throwOnError: false,
      displayMode: true
    });

    this.html =  this.sanitizer.bypassSecurityTrustHtml(equation);
  }

}
