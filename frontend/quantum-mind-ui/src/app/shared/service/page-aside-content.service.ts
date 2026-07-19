import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({providedIn: "root"})
export class PageAsideService {
  private currentSectionIdSubject = new BehaviorSubject<string | null>(null)

  constructor(){}

  setCurrentSectionId(id: string): void{
    this.currentSectionIdSubject.next(id);
  }

  get getCurrentSectionId$(): Observable<string | null>{
    return this.currentSectionIdSubject.asObservable();
  }
}
