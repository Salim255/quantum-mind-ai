import { Component, Input } from "@angular/core";

@Component({
    selector: 'app-quiz-header',
    standalone: false,
    templateUrl: './quiz-header.component.html',
    styleUrl: './quiz-header.component.scss'
})
export class QuizHeaderComponent {

    @Input({ required: true })
    quizType!: string;

    @Input({ required: true })
    topic!: string;

    @Input()
    description?: string;

}
