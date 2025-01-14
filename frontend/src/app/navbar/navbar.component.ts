import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators'; 
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { UserService, User } from '../services/user.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.component.html',
  styles: ``
})

export class NavbarComponent {
  isLoggedIn$!: Observable<boolean>;
  isAdmin$!: Observable<boolean>;
  username$!: Observable<string | null>;

  constructor(private authService: AuthService, private userService: UserService, private router: Router) {}

  ngOnInit(): void {
    this.isLoggedIn$ = this.authService.isLoggedIn$;
    this.username$ = this.userService.user$.pipe(map((user: User | null) => user ? user.username : null));
    this.isAdmin$ = this.userService.user$.pipe(map((user: User | null) => user ? user.is_admin : false));
  }

  logout() {
    this.authService.logout();    
    this.router.navigate(['/login']);
  }
}
