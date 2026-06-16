import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({providedIn: "root"})
export class PageAsideService {
  private currentIdSubject = new BehaviorSubject<string | null>(null)

  constructor(){}

  setCurrentId(id: string): void{
    this.currentIdSubject.next(id);
  }

  get getCurrentId$(): Observable<string | null>{
    return this.currentIdSubject.asObservable();
  }
}
