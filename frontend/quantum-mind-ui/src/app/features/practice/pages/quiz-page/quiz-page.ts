import { Component } from "@angular/core";

@Component({
  selector: "app-quiz-page",
  templateUrl: "./quiz-page.html",
  styleUrls: ["./quiz-page.scss"],
  standalone: false
})
export class QuizPage {
  quiz = {

    type: 'General Quiz',

    topic: 'Quantum Gates',

    description:
        'Test your understanding of fundamental quantum operations.',


    questions: [

        {
            id: 'q1',

            text:
            'Which quantum gate creates a superposition from the |0⟩ state?',


            type: 'single',


            answers: [

                {
                    id: 'a1',
                    title: 'Hadamard Gate',
                    description:
                    'Creates a superposition of |0⟩ and |1⟩.'
                },

                {
                    id: 'a2',
                    title: 'Pauli-X Gate',
                    description:
                    'Flips the state of a qubit.'
                },


                {
                    id: 'a3',
                    title: 'CNOT Gate',
                    description:
                    'Applies a controlled operation.'
                }

            ]

        }

    ]

};


 currentQuestionIndex = 0;



  selectedAnswerId?: string;


  selectedIds: string[] = [];



  get currentQuestion(): QuizQuestion {

    return this.quiz.questions[
      this.currentQuestionIndex
    ];

  }



  get canGoPrevious(): boolean {

    return this.currentQuestionIndex > 0;

  }



  get canGoNext(): boolean {

    return (
      this.currentQuestionIndex <
      this.quiz.questions.length - 1
    );

  }



  get canCheckAnswer(): boolean {

    if(this.currentQuestion.type === 'single'){

      return !!this.selectedAnswerId;

    }


    return this.selectedIds.length > 0;

  }



  onSingleAnswerSelected(id: string): void {

    this.selectedAnswerId = id;

  }



  onMultipleAnswersChanged(ids: string[]): void {

    this.selectedIds = ids;

  }



  previousQuestion(): void {

    if(this.canGoPrevious){

      this.currentQuestionIndex--;

      this.resetSelection();

    }

  }



  nextQuestion(): void {

    if(this.canGoNext){

      this.currentQuestionIndex++;

      this.resetSelection();

    }

  }



  checkAnswer(): void {

    console.log(
      'Check answer'
    );

    /*
      Later:

      - validate answer
      - show explanation
      - update score
    */

  }



  private resetSelection(): void {

    this.selectedAnswerId = undefined;

    this.selectedIds = [];

  }

}
