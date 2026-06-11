import { Observable } from "rxjs";
import { LearnHttpService } from "./learn-http.service";

export class LearnService {
  constructor(private learnHttpService: LearnHttpService){}

  getDoc(file: File): Observable<any>{
    const formData = new FormData()
    formData.append('file', file)
    return  this.learnHttpService.getDocs(formData)
  }
}
