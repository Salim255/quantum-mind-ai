import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  HostListener,
  input,
  OnDestroy,
  OnInit,
  output,
  signal,
} from '@angular/core';
import { MobileMenuService } from '../../../dashboard/services/mobile-menu.service';
import { Subscription } from 'rxjs';

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
export class AppOverlayComponent implements OnInit, OnDestroy{
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


  private isMobileMenuOpenSubscription!: Subscription;
  isMobileMenuOpen = signal(false);

  constructor(private mobileMenuService: MobileMenuService){}

  ngOnInit(): void {
    this.subscribeToMobileMenu();
  }
  protected close(): void {

    this.closed.emit();
  }

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
    
    if (this.open() && this.isMobileMenuOpen() ){
      this.mobileMenuService.close();
    }
    
    if (!this.open()) {
      return;
    }

    if (!this.closeOnEscape()) {
      return;
    }

    this.close();
  }

  private subscribeToMobileMenu(){
    this.isMobileMenuOpenSubscription = this.mobileMenuService
    .isOpen$
    .subscribe(stat => {
      this.isMobileMenuOpen.set(stat);
    });
  }

  ngOnDestroy(): void {
    this.isMobileMenuOpenSubscription?.unsubscribe();
  }
}
