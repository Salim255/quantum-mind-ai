import {
  Directive,
  ElementRef,
  EventEmitter,
  HostListener,
  Output,
} from '@angular/core';

@Directive({
  selector: '[appResizeHandle]',
  standalone: true,
})
export class ResizeHandleDirective {

  @Output()
  readonly resize = new EventEmitter<number>();

  private startX = 0;

  private startSize = 0;

  private isResizing = false;


  constructor(
    private readonly elementRef: ElementRef<HTMLElement>,
  ) {}


  @HostListener('pointerdown', ['$event'])
  onPointerDown(event: PointerEvent): void {

    event.preventDefault();

    this.isResizing = true;

    this.startX = event.clientX;

    this.startSize =
      this.elementRef.nativeElement.parentElement
        ?.getBoundingClientRect()
        .width ?? 0;

    this.elementRef.nativeElement.setPointerCapture(
      event.pointerId,
    );
  }


  @HostListener('pointermove', ['$event'])
  onPointerMove(event: PointerEvent): void {

    if (!this.isResizing) {
      return;
    }

    const delta =
      this.startX - event.clientX;

    const size =
      this.startSize + delta;

    this.resize.emit(size);
  }


  @HostListener('pointerup', ['$event'])
  onPointerUp(event: PointerEvent): void {

    if (!this.isResizing) {
      return;
    }

    this.isResizing = false;

    this.elementRef.nativeElement.releasePointerCapture(
      event.pointerId,
    );
  }


  @HostListener('pointercancel')
  onPointerCancel(): void {

    this.isResizing = false;
  }
}
