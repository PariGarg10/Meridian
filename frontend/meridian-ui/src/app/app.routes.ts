import { Routes } from '@angular/router';
import { DashboardComponent }      from './components/dashboard/dashboard.component';
import { UploadComponent }         from './components/upload/upload.component';
import { ForecastResultComponent } from './components/forecast-result/forecast-result.component';

export const routes: Routes = [
  { path: '',              component: DashboardComponent      },
  { path: 'upload',        component: UploadComponent         },
  { path: 'result/:jobId', component: ForecastResultComponent },
];