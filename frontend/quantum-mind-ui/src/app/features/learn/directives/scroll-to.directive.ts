import { Directive, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[appScrollTo]'
})
export class ScrollToDirective {
  @Input('appScrollTo') targetId!: string;

  @HostListener('click', ['$event'])
  onClick(event: Event) {
    event.preventDefault();

    const container = document.querySelector('.learn-page__content') as HTMLElement | null;
    const target = document.getElementById(this.targetId) as HTMLElement | null;

    if (!container || !target) return;

    const top = target.offsetTop - container.offsetTop;

    container.scrollTo({
      top,
      behavior: 'smooth'
    });
  }
}
