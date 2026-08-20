import {
  ChangeDetectionStrategy,
  Component,
  Input,
} from '@angular/core';

@Component({
  selector: 'app-practice-overview-section',
  standalone: false,
  templateUrl: './practice-overview-section.component.html',
  styleUrl: './practice-overview-section.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticeOverviewSectionComponent {

  @Input({ required: true })
  eyebrow!: string;

  @Input({ required: true })
  title!: string;

  @Input()
  description?: string;

  @Input()
  actionLabel?: string;

  @Input()
  actionLink?: string;

  @Input()
  labelledBy?: string;

}