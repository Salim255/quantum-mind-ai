import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class MobileMenuService {

  /* ==========================================================
  STATE
  ========================================================== */
  private readonly isOpenSubject =
    new BehaviorSubject<boolean>(false);


  /* ==========================================================
  PUBLIC STATE
  ========================================================== */
  readonly isOpen$ = this.isOpenSubject.asObservable();


  /* ==========================================================
  ACTIONS
  ========================================================== */
  open(): void {
    this.isOpenSubject.next(true);
  }

  close(): void {
    this.isOpenSubject.next(false);
  }

  toggle(): void {
    this.isOpenSubject.next(
      !this.isOpenSubject.value
    );
  }
}