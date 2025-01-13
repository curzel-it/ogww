import { Component, OnInit } from '@angular/core';
import { ApiService, Site } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  sites: Site[] = [];
  errorMessage: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.getUserSites().subscribe({
      next: (data) => (this.sites = data),
      error: (err) => {
        console.error(err);
        this.errorMessage = 'Failed to load sites';
      },
    });
  }
}
