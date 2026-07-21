import { Component } from "@angular/core";
import { QuizQuestion } from "./models/quiz.model";

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
        'Test your understanding of the fundamental gates used in quantum computing.',

    questions: [

        {
            id: 'q1',

            text:
                'Which quantum gate creates an equal superposition from the |0⟩ state?',

            description:
                'Select the single best answer.',

            type: 'multiple',

            answers: [

                {
                    id: 'a1',

                    title: 'Hadamard Gate',

                    hint:
                        'Think about the gate that transforms basis states into equal probability amplitudes.',

                    correctExplanation:
                        'Correct. The Hadamard gate transforms |0⟩ into (|0⟩ + |1⟩)/√2, creating an equal superposition.',

                    incorrectExplanation:
                        'The Hadamard gate is actually the correct answer.',

                    isCorrect: true
                },

                {
                    id: 'a2',

                    title: 'Pauli-X Gate',

                    hint:
                        'Does this gate create a new quantum state or simply flip an existing one?',

                    correctExplanation:
                        '',

                    incorrectExplanation:
                        'The Pauli-X gate behaves like a classical NOT gate. It flips |0⟩ to |1⟩ but does not create a superposition.',

                    isCorrect: false
                },

                {
                    id: 'a3',

                    title: 'CNOT Gate',

                    hint:
                        'Consider how many qubits this gate requires.',

                    correctExplanation:
                        '',

                    incorrectExplanation:
                        'CNOT is a two-qubit gate. By itself, it does not create a superposition from a single |0⟩ qubit.',

                    isCorrect: false
                },

                {
                    id: 'a4',

                    title: 'SWAP Gate',

                    hint:
                        'Does this gate modify amplitudes or only exchange qubits?',

                    correctExplanation:
                        '',

                    incorrectExplanation:
                        'The SWAP gate exchanges the states of two qubits. It does not generate superposition.',

                    isCorrect: false
                }

            ]

        },

        {

            id: 'q2',

            text:
                'Which of the following are single-qubit quantum gates?',

            description:
                'Select all correct answers.',

            type: 'multiple',

            answers: [

                {

                    id: 'a1',

                    title: 'Hadamard Gate',

                    hint:
                        'This gate acts on only one qubit.',

                    correctExplanation:
                        'Correct. Hadamard is a single-qubit gate.',

                    incorrectExplanation:
                        '',

                    isCorrect: true

                },

                {

                    id: 'a2',

                    title: 'Pauli-X Gate',

                    hint:
                        'Think of the quantum equivalent of a NOT gate.',

                    correctExplanation:
                        'Correct. Pauli-X is a single-qubit gate.',

                    incorrectExplanation:
                        '',

                    isCorrect: true

                },

                {

                    id: 'a3',

                    title: 'CNOT Gate',

                    hint:
                        'Count how many qubits participate in this operation.',

                    correctExplanation:
                        '',

                    incorrectExplanation:
                        'CNOT requires both a control qubit and a target qubit.',

                    isCorrect: false

                },

                {

                    id: 'a4',

                    title: 'Toffoli Gate',

                    hint:
                        'This gate involves more than one control qubit.',

                    correctExplanation:
                        '',

                    incorrectExplanation:
                        'The Toffoli gate operates on three qubits, so it is not a single-qubit gate.',

                    isCorrect: false

                }

            ]

        }

    ]

};


 currentQuestionIndex = 0;



  selectedAnswerId?: string;


  selectedIds: string[] = [];



  get currentQuestion(): QuizQuestion {
    return  (this.quiz.questions as QuizQuestion[])[this.currentQuestionIndex]
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
