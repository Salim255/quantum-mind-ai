import { Topic } from "../models/topic.model";

export interface ExploreCategory {
    name: string;
    description: string;
    topics: Topic[];
}
