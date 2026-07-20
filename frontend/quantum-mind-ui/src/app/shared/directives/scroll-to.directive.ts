import { Directive, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[appScrollTo]',
  standalone: false
})
export class ScrollToDirective {
  @Input('appScrollTo') targetId!: string;
  @Input() scrollContainer!: HTMLElement; // 👈 container passed from component

  @HostListener('click', ['$event'])
  onClick(event: Event) {
    event.preventDefault();

    console.log("hello from directive", this.targetId, this.scrollContainer)
    const container = this.scrollContainer;
    const target = document.getElementById(this.targetId) as HTMLElement | null;

    if (!container || !target) return;
     //const top = target.getBoundingClientRect().top + container.scrollTop;
    const top = target.offsetTop;
    container.scrollTo({
      top,
      behavior: 'smooth'
    });
  }
}
