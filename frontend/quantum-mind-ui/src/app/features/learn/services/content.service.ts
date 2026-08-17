import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({providedIn: "root"})
export class ContentService {

  private currentSectionsSubject = new BehaviorSubject< { name: string, id: string } []>(
    JSON.parse(localStorage.getItem('asideSections') ?? '[]')
  );

  setPageAsideContent(sections: { name: string, id: string } []) {
    localStorage.setItem("asideSections",JSON.stringify(sections));
    this.currentSectionsSubject.next(sections);
  }

  get getPageAsideContent$(): Observable<{ name: string, id: string } []>{
    return this.currentSectionsSubject.asObservable()
  }

  clearStorage(): void{
    localStorage.removeItem("asideSections")
  }
}
