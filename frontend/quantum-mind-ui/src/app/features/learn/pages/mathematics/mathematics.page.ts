import { Component, OnInit, signal } from "@angular/core";
import { LearnService } from "../../services/learn.service";
import { DomSanitizer } from "@angular/platform-browser";


@Component({
  selector: "app-mathematics",
  templateUrl: "./mathematics.page.html",
  styleUrls: ["./mathematics.page.scss"],
  standalone: false
})
export class MathematicsPage implements OnInit {
  htmlSections = signal<any[]>([]);

  constructor(
    private sanitizer: DomSanitizer,
    private learnService: LearnService
  ){}

  ngOnInit(): void {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    this.learnService.getDoc(file).subscribe({
      next: (res) => {
        const html = res.html;
        console.log(html, res);
      // res is an array of sections
          const safeSections = res.map((section: any) => ({
            ...section,
            html: this.sanitizer.bypassSecurityTrustHtml(section.html)
          }));

          this.htmlSections.set(safeSections);
      },
      error: (err) => console.log(err)
    });
  }

  equation =
    'H|0\\rangle = \\frac{1}{\\sqrt{2}} (|0\\rangle + |1\\rangle)';
}
