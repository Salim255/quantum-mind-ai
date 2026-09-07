import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({providedIn: 'root'})
export class AttemptResultService {
  private resultModalState = new BehaviorSubject<boolean>(false)


  private setAttemptResult(status: boolean){
    this.resultModalState.next(status)
  }

  dismissResult(){

    this.setAttemptResult(false)
  }

  showResult(){
    this.setAttemptResult(true)
  }

  get getShowResult$(): Observable<boolean>{
    return this.resultModalState.asObservable();
  }
}