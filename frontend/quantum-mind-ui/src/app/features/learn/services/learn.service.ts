import { BehaviorSubject, map, Observable, of, tap } from "rxjs";
import { LearnHttpService } from "./learn-http.service";
import { Injectable } from "@angular/core";
import { TopicsResponseDTO } from "../interfaces/topics-response.dto";
import { ApiResponseDTO } from "../../../shared/interfaces/api-response.dto";
import { TopicWithSectionsDTO } from "../interfaces/topic-with-sections.dto";

@Injectable({providedIn: "root"})
export class LearnService {
  private learnTopicSubject = new BehaviorSubject<TopicWithSectionsDTO[]>([])
  getLearnTopics$ = this.learnTopicSubject.asObservable();

  constructor(private learnHttpService: LearnHttpService){}

  getDoc(file: File): Observable<any>{
    const formData = new FormData()
    formData.append('file', file)
    return  this.learnHttpService.getDocs(formData)
  }

  getTopics():Observable<ApiResponseDTO<TopicsResponseDTO>>{
    return this.learnHttpService.getLearnTopics().pipe(
      tap((response) => {
        const topics = response.data.topics;
        this.learnTopicSubject.next(topics);
      })
    );
  }


  getTopicItem$(topicOrder: number): Observable<TopicWithSectionsDTO | null> {
    return this.getLearnTopics$.pipe(
      map((topics) => {
        if (!topics) {
          return null
        } else {
          const topic: TopicWithSectionsDTO | undefined =
            topics.find(t => t.display_order === topicOrder);

          return topic || null
        }
      })
    )
  }

}
