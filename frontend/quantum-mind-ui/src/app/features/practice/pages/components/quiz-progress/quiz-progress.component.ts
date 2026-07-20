@Component({
    selector: 'app-quiz-progress',
    standalone: false,
    templateUrl: './quiz-progress.component.html',
    styleUrl: './quiz-progress.component.scss'
})
export class QuizProgressComponent {

    @Input({ required: true })
    current!: number;

    @Input({ required: true })
    total!: number;

    get progress(): number {
        return (this.current / this.total) * 100;
    }

}
