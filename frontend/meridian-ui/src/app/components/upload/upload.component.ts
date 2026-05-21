import { Component }    from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule }  from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Router }       from '@angular/router';
import { ForecastService } from '../../services/forecast.service';

@Component({
  selector:    'app-upload',
  templateUrl: './upload.component.html',
  styleUrls:   ['./upload.component.scss'],
  standalone:  true,
  imports:     [CommonModule, FormsModule, RouterModule]
})
export class UploadComponent {

  tenantId     = '';
  datasetRef   = 'data/passengers.csv';
  horizonDays  = 12;
  isSubmitting = false;
  errorMsg     = '';

  horizonOptions = [
    { label: '3 months',  value: 3  },
    { label: '6 months',  value: 6  },
    { label: '12 months', value: 12 },
    { label: '24 months', value: 24 },
  ];

  constructor(
    private forecastService: ForecastService,
    private router: Router
  ) {}

  submitJob() {
    if (!this.tenantId) return;
    this.isSubmitting = true;
    this.errorMsg     = '';

    this.forecastService.submitJob({
      tenantId:    this.tenantId,
      datasetRef:  this.datasetRef,
      horizonDays: this.horizonDays
    }).subscribe({
      next: (response) => {
        const saved = localStorage.getItem('meridian_jobs');
        const jobs  = saved ? JSON.parse(saved) : [];
        jobs.unshift({ jobId: response.jobId, tenantId: this.tenantId, status: response.status });
        localStorage.setItem('meridian_jobs', JSON.stringify(jobs.slice(0, 10)));
        this.router.navigate(['/result', response.jobId]);
      },
      error: () => {
        this.isSubmitting = false;
        this.errorMsg = 'Could not connect to server. Make sure Python server is running.';
      }
    });
  }
}