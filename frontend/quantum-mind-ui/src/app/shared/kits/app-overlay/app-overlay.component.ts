import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  HostListener,
  input,
  output,
} from '@angular/core';

export type OverlayWidth =
  | 'sm'
  | 'md'
  | 'lg'
  | 'full';

@Component({
  selector: 'app-overlay',
  standalone: false,

  templateUrl: './app-overlay.component.html',
  styleUrl: './app-overlay.component.scss',
})
export class AppOverlayComponent {

  /* ==========================================================
     STATE
  ========================================================== */

  readonly open = input(false);


  /* ==========================================================
     CONTENT
  ========================================================== */

  readonly title = input<string | null>(null);

  readonly subtitle = input<string | null>(null);


  /* ==========================================================
     CONTROLS
  ========================================================== */

  readonly showClose = input(true);

  readonly closeOnBackdrop = input(true);

  readonly closeOnEscape = input(true);


  /* ==========================================================
     SIZE
  ========================================================== */

  readonly width = input<OverlayWidth>('md');


  /* ==========================================================
     EVENTS
  ========================================================== */

  readonly closed = output<void>();


  /* ==========================================================
     CLOSE
  ========================================================== */

  protected close(): void {

    this.closed.emit();
  }


  /* ==========================================================
     BACKDROP
  ========================================================== */

  protected onBackdropClick(): void {

    if (!this.closeOnBackdrop()) {
      return;
    }

    this.close();
  }


  /* ==========================================================
     ESCAPE
  ========================================================== */

  @HostListener('document:keydown.escape')
  protected onEscape(): void {

    if (!this.open()) {
      return;
    }

    if (!this.closeOnEscape()) {
      return;
    }

    this.close();
  }
}
