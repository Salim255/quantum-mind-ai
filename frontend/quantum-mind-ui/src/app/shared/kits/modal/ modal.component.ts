import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  input,
} from '@angular/core';

import {
  CommonModule,
  NgComponentOutlet,
} from '@angular/common';

import { ModalConfig } from './modal-config';


@Component({
  selector: 'app-modal',
  standalone: false,
  templateUrl: './modal.component.html',
  styleUrl: './modal.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ModalComponent {

  readonly config =
    input.required<ModalConfig>();


  protected close(): void {

    // For now, the parent controls whether
    // the modal is rendered.
  }
}
