import {
  ChangeDetectionStrategy,
  Component,
  output,
  input,
} from '@angular/core';

@Component({
  selector: 'app-sidebar-toggle',
  standalone: false,
  templateUrl: './sidebar-toggle.component.html',
  styleUrl: './sidebar-toggle.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SidebarToggleComponent {

  readonly collapsed = input(false);

  readonly toggled = output<void>();


  protected toggle(): void {
    this.toggled.emit();
  }
}