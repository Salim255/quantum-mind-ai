import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SidebarToggleService {

  private readonly _collapsedSubject =
    new BehaviorSubject<boolean>(false);


  readonly collapsed$ =
    this._collapsedSubject.asObservable();


  get collapsed(): boolean {

    return this._collapsedSubject.value;
  }


  set collapsed(value: boolean) {

    this._collapsedSubject.next(value);
  }


  toggle(): void {

    this.collapsed =
      !this.collapsed;
  }
}