import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  signal,
} from '@angular/core';

import {
  EventType,
  NavigationEnd,
  Router,
} from '@angular/router';

import { filter } from 'rxjs';

import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { SidebarToggleService } from '../../services/sidebar-toggle.service';


@Component({
  selector: 'app-sidebar-toggle',
  standalone: false,
  templateUrl: './sidebar-toggle.component.html',
  styleUrl: './sidebar-toggle.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SidebarToggleComponent {

  /* ============================================================
     STATE
  ============================================================ */

  protected readonly collapsed = signal(false);

  protected readonly available = signal(false);


  /* ============================================================
     DEPENDENCIES
  ============================================================ */

  private readonly destroyRef = inject(DestroyRef);


  constructor(
    private readonly router: Router,
    private readonly sidebarToggleService: SidebarToggleService,
  ) {

    this.listenToSidebarToggle();

    this.listenToRouter();
  }


  /* ============================================================
     TOGGLE
  ============================================================ */

  protected toggle(): void {

    if (!this.available()) {
      return;
    }

    this.sidebarToggleService.toggle();
  }


  /* ============================================================
     SIDEBAR TOGGLE STATE
  ============================================================ */

  private listenToSidebarToggle(): void {

    this.sidebarToggleService.collapsed$
      .pipe(
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(collapsed => {

        this.collapsed.set(collapsed);
      });
  }


  /* ============================================================
     ROUTER
  ============================================================ */

  private listenToRouter(): void {

    this.router.events
      .pipe(
        filter(
          (event): event is NavigationEnd =>
            event.type === EventType.NavigationEnd
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(event => {

        const url =
          event.urlAfterRedirects === '/'
            ? '/home'
            : event.urlAfterRedirects;

        this.updateAvailability(url);
      });


    // Initialize immediately for the current route.
    this.updateAvailability(this.router.url);
  }


  /* ============================================================
     AVAILABILITY
  ============================================================ */

  private updateAvailability(url: string): void {

    this.available.set(
      this.hasSecondarySidebar(url),
    );
  }


  /* ============================================================
     SECONDARY SIDEBAR ROUTES
  ============================================================ */

  private hasSecondarySidebar(url: string): boolean {

    return [
      '/learn',
      '/quizzes',
    ].some(route =>
      url === route ||
      url.startsWith(`${route}/`)
    );
  }
}