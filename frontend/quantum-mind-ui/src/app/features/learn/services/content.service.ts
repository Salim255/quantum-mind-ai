import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({providedIn: "root"})
export class ContentService {
  private currentSectionsSubject = new BehaviorSubject< { name: string } []>([]) ;

  setPageAsideContent(sections: { name: string } []){
    this.currentSectionsSubject.next(sections);
  }

  get getPageAsideContent$(): Observable<{ name: string } []>{
    return this.currentSectionsSubject.asObservable()
  }
}
