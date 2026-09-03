
interface AttemptAnswer {

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


interface AttemptQuestion {

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


interface Attempt {

  id: string;

  user_id: string | null;

  topic_id: string;

  topic: Topic & {

    questions: AttemptQuestion[];

  };
}