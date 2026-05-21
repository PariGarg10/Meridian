import { Component }        from '@angular/core';
import { RouterOutlet }     from '@angular/router';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule }     from '@angular/common';
import { FormsModule }      from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { NavbarComponent }         from './components/navbar/navbar.component';
import { DashboardComponent }      from './components/dashboard/dashboard.component';
import { UploadComponent }         from './components/upload/upload.component';
import { ForecastResultComponent } from './components/forecast-result/forecast-result.component';
import { JobStatusComponent }      from './components/job-status/job-status';

@Component({
  selector:    'app-root',
  templateUrl: './app.html',
  styleUrls:   ['./app.scss'],
  standalone:  true,
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    CommonModule,
    FormsModule,
    HttpClientModule,
    NavbarComponent,
    DashboardComponent,
    UploadComponent,
    ForecastResultComponent,
    JobStatusComponent,
  ]
})
export class App {
  title = 'meridian-ui';
}