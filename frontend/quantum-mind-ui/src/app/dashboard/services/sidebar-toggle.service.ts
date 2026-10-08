import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SidebarToggleService {
  private readonly storageKey = 'sidebarCollapsed';

  private readonly _collapsedSubject =
    new BehaviorSubject<boolean>(this.getInitialCollapsedState());

  readonly collapsed$ =
    this._collapsedSubject.asObservable();

  get collapsed(): boolean {
    return this._collapsedSubject.value;
  }

  set collapsed(value: boolean) {
    this._collapsedSubject.next(value);
    localStorage.setItem(
      this.storageKey,
      JSON.stringify(value)
    );
  }

  toggle(): void {
    this.collapsed = !this.collapsed;
  }

  setCollapsed(value: boolean): void {
    this.collapsed = value;
  }

  private getInitialCollapsedState(): boolean {
    const savedState = localStorage.getItem(this.storageKey);

    if (savedState === null) {
      return false;
    }

    try {
      return JSON.parse(savedState);
    } catch {
      return false;
    }
  }
}
