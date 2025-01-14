import { Injectable } from '@angular/core';
import {
  CanActivate,
  UrlTree,
  Router
} from '@angular/router';
import { Observable, combineLatest, of } from 'rxjs';
import { map, take } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { UserService } from '../services/user.service';

@Injectable({
  providedIn: 'root',
})
export class AdminGuard implements CanActivate {
  constructor(
    private authService: AuthService, 
    private userService: UserService, 
    private router: Router
) {}
  canActivate():
    | Observable<boolean | UrlTree>
    | Promise<boolean | UrlTree>
    | boolean
    | UrlTree {
    return combineLatest([this.authService.isLoggedIn$, this.userService.isAdmin$]).pipe(
      take(1),
      map(([isLoggedIn, isAdmin], _) => {
        console.log(`isLoggedIn ${isLoggedIn} isAdmin ${isAdmin}`);

        if (isLoggedIn && isAdmin) {
          return true;
        }
        return this.router.createUrlTree(['/unauthorized']);
      })
    );
  }
}
