import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, switchMap, catchError } from 'rxjs';
import { AuthService } from '../auth.service'
import { of } from 'rxjs';

export type User = {
  id: string,
  email: string,
  is_admin: boolean,
  username: string
};

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private userUrl = 'http://localhost:8000/users/me/';
  
  private userSubject = new BehaviorSubject<User | null>(null);
  public user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient, private authService: AuthService) {
    this.authService.isLoggedIn$.pipe(
      switchMap(isLoggedIn => {
        if (isLoggedIn) {
          return this.fetchUser();
        } else {
          this.userSubject.next(null);
          return of(null);
        }
      }),
      catchError(error => {
        console.error('Error fetching user data:', error);
        this.userSubject.next(null);
        return of(null);
      })
    ).subscribe(user => {
      if (user) {
        this.userSubject.next(user);
      }
    });
  }

  private fetchUser(): Observable<User> {
    return this.http.get<User>(this.userUrl);
  }

  refreshUser(): void {
    if (this.authService.isLoggedIn$) {
      this.fetchUser().subscribe({
        next: (user) => this.userSubject.next(user),
        error: (err) => {
          console.error('Failed to refresh user data', err);
          this.userSubject.next(null);
          this.authService.logout();
        },
      });
    } else {
      this.userSubject.next(null);
    }
  }
}
