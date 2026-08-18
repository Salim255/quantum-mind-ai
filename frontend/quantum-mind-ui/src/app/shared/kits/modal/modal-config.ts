import { Type } from '@angular/core';

export type ModalSize =
  | 'sm'
  | 'md'
  | 'lg'
  | 'full';

export interface ModalConfig<T = unknown> {

  component: Type<T>;

  data?: unknown;

  title?: string;

  subtitle?: string;

  showClose?: boolean;

  closeOnBackdrop?: boolean;

  closeOnEscape?: boolean;

  size?: ModalSize;
}
