export type QuizQuestionType =
    | 'single'
    | 'multiple';



export interface QuizAnswer {

    /**
     * Unique identifier of the answer.
     * Used for selection tracking.
     */
    id: string;


    /**
     * Main answer text displayed to the learner.
     */
    title: string;


    /**
     * Optional explanation or additional context.
     */
    description?: string;

    hint?: string;

    incorrectExplanation?: string;

    correctExplanation?: string;

    isCorrect: boolean;

}



export interface QuizQuestion {

    /**
     * Unique question identifier.
     */
    id: string;


    /**
     * The question displayed to the user.
     */
    text: string;

    description?: string;
    /**
     * Defines the selection behavior.
     */
    type: QuizQuestionType;


    /**
     * Available choices.
     */
    answers: QuizAnswer[];

}
