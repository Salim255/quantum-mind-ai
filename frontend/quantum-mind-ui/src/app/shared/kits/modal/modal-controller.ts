import { Injectable } from '@angular/core';
import { ModalOptions } from './modal.types';
import { ModalRef } from './modal-ref';


@Injectable({ providedIn: 'root' })
export class ModalController {

  /* ==========================================================
     ACTIVE MODAL
  ========================================================== */

  private activeModal:
    ModalRef<unknown> | null = null;


  /* ==========================================================
     CREATE
  ========================================================== */

  async create<
    TData = unknown,
    TResult = unknown,
  >(
    options: ModalOptions<TData>,
  ): Promise<ModalRef<TResult>> {

    /*
     * Create a reference for this modal instance.
     */
    const modalRef =
      new ModalRef<TResult>();


    /*
     * Keep track of the currently active modal.
     */
    this.activeModal =
      modalRef as ModalRef<unknown>;


    /*
     * Once the modal is dismissed, remove it
     * from the active modal reference.
     */
    modalRef.onDidDismiss.subscribe(() => {

      if (
        this.activeModal === modalRef
      ) {

        this.activeModal = null;
      }
    });


    return modalRef;
  }


  /* ==========================================================
     DISMISS ACTIVE MODAL
  ========================================================== */

  async dismiss<TResult = unknown>(
    data?: TResult,
    role?: string,
  ): Promise<boolean> {

    if (!this.activeModal) {
      return false;
    }


    this.activeModal.dismiss(
      data,
      role,
    );


    this.activeModal = null;

    return true;
  }


  /* ==========================================================
     GET ACTIVE MODAL
  ========================================================== */

  getTop():
    ModalRef<unknown> | null {

    return this.activeModal;
  }
}
