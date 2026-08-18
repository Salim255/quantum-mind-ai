import { Subject } from 'rxjs';

import {
  ModalDismissResult,
} from './modal.types';


export class ModalRef<TResult = unknown> {

  /* ==========================================================
     DISMISS STATE
  ========================================================== */

  private readonly dismissSubject =
    new Subject<ModalDismissResult<TResult>>();


  /* ==========================================================
     DISMISS RESULT
  ========================================================== */

  readonly onDidDismiss =
    this.dismissSubject.asObservable();


  /* ==========================================================
     DISMISS
  ========================================================== */

  dismiss(
    data?: TResult,
    role?: string,
  ): void {

    this.dismissSubject.next({
      data,
      role,
    });

    this.dismissSubject.complete();
  }
}
