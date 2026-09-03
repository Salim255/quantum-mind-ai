import { Attempt } from "../../attempt/interfaces/attempt.interface";
import { Topic } from "../models/topic.model";


export interface ExploreTopicDTO {

  /*
   * ==========================================================
   * TOPIC
   * ==========================================================
   *
   * The topic being displayed in Explore.
   */
  topic: Topic;


  /*
   * ==========================================================
   * LATEST ATTEMPT
   * ==========================================================
   *
   * The current user's latest attempt for this topic.
   *
   * null means that the user has never attempted this topic.
   *
   * When present, the Attempt contains its own metadata,
   * including its status.
   */
  latestAttempt: Attempt | null;

}

export interface ExploreState {
  topics:  ExploreTopicDTO[];
}