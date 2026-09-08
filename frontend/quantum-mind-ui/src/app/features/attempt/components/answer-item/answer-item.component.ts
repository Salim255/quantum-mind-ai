import {
  ChangeDetectionStrategy,
  Component,
  input,
  OnDestroy,
  OnInit,
  output,
} from '@angular/core';
import { AttemptAnswer } from '../../interfaces/attempt.interface';
import { AttemptService } from '../../services/attempt.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-answer-item',
  standalone: false,
  templateUrl: './answer-item.component.html',
  styleUrl: './answer-item.component.scss',
})
export class AnswerItemComponent {

  readonly answer = input.required<AttemptAnswer>();

  readonly index = input.required<number>();


  readonly selected = input<boolean>(false);

  readonly answerSelected = output<AttemptAnswer['id']>();

  protected readonly isSelected = () => this.selected();

  protected select(): void {
    this.answerSelected.emit(this.answer().id);
  }

}