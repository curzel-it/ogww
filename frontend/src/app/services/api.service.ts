import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Site {
  id: string;
  name: string;
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getUserSites(): Observable<Site[]> {
    return this.http.get<Site[]>(`${this.apiUrl}/sites/`);
  }
}
