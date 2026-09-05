// topic.model.ts

import { AttemptQuestion } from "../../attempt/interfaces/attempt.interface";

export interface Topic {
  id: string;
  title: string;
  slug: string;
  category: string;
  display_order: number;
  description: string;

  questions: AttemptQuestion [] | null
}