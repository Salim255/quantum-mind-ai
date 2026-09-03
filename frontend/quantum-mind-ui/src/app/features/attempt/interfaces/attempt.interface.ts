import { Topic } from "../../explore/models/topic.model";


export interface AttemptResponseDTO {
  attempt: Attempt;
}


export interface AttemptAnswer {

  id: string;

  question_id: string;

  text: string;

  explanation: string | null;

  is_correct: boolean;

  display_order: number;

  is_active: boolean;

  created_at: string;

  updated_at: string;
}


export interface AttemptQuestion {

  id: string;

  topic_id: string;

  text: string;

  explanation: string;

  difficulty: string;

  display_order: number;

  source: string;

  is_active: boolean;

  answers: AttemptAnswer[];

  created_at: string;

  updated_at: string;
}


// ============================================================
// ATTEMPT
// ============================================================

export interface Attempt {

  id: string;

  user_id: string | null;

  topic_id: string;

  topic: Topic;

  score: number;

  total_questions: number;

  correct_answers: number;

  is_completed: boolean;

  started_at: string;

  completed_at: string | null;

  attempt_questions: AttemptQuestion[];
}