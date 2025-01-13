// src/app/app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

// Routing Module
import { AppRoutingModule } from './app-routing.module';

// Root Component
import { AppComponent } from './app.component';

// Feature Components
import { LoginComponent } from './components/login/login.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';

// Services and Interceptors
import { AuthInterceptor } from './interceptors/auth.interceptor';

// Guards
import { AuthGuard } from './guards/auth.guard'; // Ensure AuthGuard is properly implemented and imported

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    // ... add other components here
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    // ... add other modules here
  ],
  providers: [
    // Register AuthGuard if it's not providedIn: 'root'
    // AuthGuard, 

    // Register the AuthInterceptor
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true, // Allows multiple interceptors
    },
    // ... add other services here
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
