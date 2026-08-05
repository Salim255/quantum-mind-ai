import { BehaviorSubject, Observable, tap } from "rxjs";
import { LearnHttpService } from "./learn-http.service";
import { Injectable } from "@angular/core";

@Injectable({providedIn: "root"})
export class LearnService {
  private learnTopicSubject = new BehaviorSubject<any>(null)
  getLearnTopics$ = this.learnTopicSubject.asObservable();

  constructor(private learnHttpService: LearnHttpService){}

  getDoc(file: File): Observable<any>{
    const formData = new FormData()
    formData.append('file', file)
    return  this.learnHttpService.getDocs(formData)
  }

  getTopics(){
    return this.learnHttpService.getLearnTopics().pipe(
      tap((response) => {
        const topics = response.data.topics;
        this.learnTopicSubject.next(topics);
      })
    );
  }
}
