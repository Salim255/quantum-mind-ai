import {
  ChangeDetectionStrategy,
  Component,
  Input,
} from '@angular/core';
import { RouterLink } from '@angular/router';

export type PracticeOverviewTopicCardVariant =
  | 'default'
  | 'attention';

@Component({
  selector: 'app-practice-overview-topic-card',
  standalone: false,
  templateUrl: './practice-overview-topic-card.component.html',
  styleUrl: './practice-overview-topic-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PracticeOverviewTopicCardComponent {

  @Input({ required: true })
  title!: string;

  @Input({ required: true })
  description!: string;

  @Input({ required: true })
  score!: string;

  @Input({ required: true })
  icon!: string;

  @Input({ required: true })
  link!: string;

  @Input()
  variant: PracticeOverviewTopicCardVariant = 'default';
}