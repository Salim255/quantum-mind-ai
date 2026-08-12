import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class AIAssistantService {

  private readonly _isAssistantVisible$ = new BehaviorSubject<boolean>(false);

  readonly isAssistantVisible$ = this._isAssistantVisible$.asObservable();


  showAssistant(): void {
    this._isAssistantVisible$.next(true);
  }


  hideAssistant(): void {
    this._isAssistantVisible$.next(false);
  }


  toggleAssistant(): void {
    this._isAssistantVisible$.next(
      !this._isAssistantVisible$.value
    );
  }
}
