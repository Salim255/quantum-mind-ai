import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Output,
} from '@angular/core';


@Component({
  selector: 'app-attempt-result-actions',
  standalone: false,
  templateUrl: './attempt-result-actions.component.html',
  styleUrl: './attempt-result-actions.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AttemptResultActionsComponent {
  @Output()
  readonly retake = new EventEmitter<void>();

  @Output()
  readonly explore = new EventEmitter<void>();

  onRetake(): void {
    this.retake.emit();
  }

  onExplore(): void {
    this.explore.emit();
  }
}