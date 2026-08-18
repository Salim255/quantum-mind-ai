import { Type } from '@angular/core';


/* ============================================================
   MODAL WIDTH
============================================================ */

export type ModalWidth =
  | 'sm'
  | 'md'
  | 'lg'
  | 'full';


/* ============================================================
   MODAL OPTIONS
============================================================ */

export interface ModalOptions<TData = unknown> {

  /**
   * Component rendered inside the modal.
   */
  component: Type<unknown>;


  /**
   * Data passed to the component.
   */
  componentProps?: TData;


  /**
   * Optional modal title.
   */
  title?: string;


  /**
   * Optional modal subtitle.
   */
  subtitle?: string;


  /**
   * Display the close button.
   *
   * @default true
   */
  showClose?: boolean;


  /**
   * Close when clicking the backdrop.
   *
   * @default true
   */
  closeOnBackdrop?: boolean;


  /**
   * Close when pressing Escape.
   *
   * @default true
   */
  closeOnEscape?: boolean;


  /**
   * Modal width.
   *
   * @default 'md'
   */
  width?: ModalWidth;
}


/* ============================================================
   MODAL DISMISS RESULT
============================================================ */

export interface ModalDismissResult<TResult = unknown> {

  /**
   * Data returned when the modal closes.
   */
  data?: TResult;


  /**
   * Optional reason for closing.
   *
   * Examples:
   * - 'close'
   * - 'backdrop'
   * - 'escape'
   * - 'confirmed'
   * - 'cancelled'
   */
  role?: string;
}
