import { Injectable } from "@angular/core";
import { SPIN } from "./data"
@Injectable({providedIn: "root"})
export class ContentService {

  getAsideContent(){
    return SPIN
  }
}
