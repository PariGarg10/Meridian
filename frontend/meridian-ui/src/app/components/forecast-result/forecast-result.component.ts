import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';
import { RouterModule }      from '@angular/router';
import { ActivatedRoute }    from '@angular/router';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { ForecastService, ForecastResult } from '../../services/forecast.service';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector:    'app-forecast-result',
  templateUrl: './forecast-result.component.html',
  styleUrls:   ['./forecast-result.component.scss'],
  standalone:  true,
  imports:     [CommonModule, RouterModule, MatProgressBarModule, DecimalPipe]
})
export class ForecastResultComponent implements OnInit {

  isLoading    = true;
  errorMsg     = '';
  result:      ForecastResult | null = null;
  tableData:   any[] = [];
  modelScores: any[] = [];

  constructor(
    private route:           ActivatedRoute,
    private forecastService: ForecastService,
    private cdr:             ChangeDetectorRef
  ) {}

  ngOnInit() {
    const jobId = this.route.snapshot.paramMap.get('jobId')!;
    this.pollForResult(jobId);
  }

  pollForResult(jobId: string) {
    let attempts = 0;
    const maxAttempts = 40;

    const poll = setInterval(() => {
      attempts++;

      this.forecastService.getJobStatus(jobId).subscribe({
        next: (status) => {
          console.log('Job status:', status.status, 'attempt:', attempts);

          if (status.status === 'DONE') {
            clearInterval(poll);
            this.loadResult(jobId);
          } else if (status.status === 'FAILED') {
            clearInterval(poll);
            this.isLoading = false;
            this.errorMsg  = 'Forecast job failed.';
            this.cdr.detectChanges();
          } else if (attempts >= maxAttempts) {
            clearInterval(poll);
            this.isLoading = false;
            this.errorMsg  = 'Timed out.';
            this.cdr.detectChanges();
          }
        },
        error: () => {
          clearInterval(poll);
          this.isLoading = false;
          this.errorMsg  = 'Could not connect to server.';
          this.cdr.detectChanges();
        }
      });
    }, 3000);
  }

  loadResult(jobId: string) {
    this.forecastService.getResult(jobId).subscribe({
      next: (result) => {
        this.result    = result;
        this.isLoading = false;

        this.tableData = result.dates.map((date, i) => ({
          date,
          prediction: result.predictions[i],
          lower:      result.lowerBound[i],
          upper:      result.upperBound[i],
        }));

        this.modelScores = [
          { name: 'Prophet', icon: '📈', mae: result.allScores.prophet },
          { name: 'ARIMA',   icon: '📊', mae: result.allScores.arima   },
          { name: 'LSTM',    icon: '🧠', mae: result.allScores.lstm    },
        ];

        // Force Angular to re-render
        this.cdr.detectChanges();

        setTimeout(() => {
          this.drawChart(result);
          this.cdr.detectChanges();
        }, 200);
      },
      error: (err) => {
        console.log('Error:', err);
        this.isLoading = false;
        this.errorMsg  = 'Could not load result.';
        this.cdr.detectChanges();
      }
    });
  }

  drawChart(result: ForecastResult) {
    const ctx = document.getElementById('forecastChart') as HTMLCanvasElement;
    if (!ctx) return;
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: result.dates,
        datasets: [
          { label: 'Forecast',    data: result.predictions, borderColor: '#1a73e8', backgroundColor: 'rgba(26,115,232,0.1)', borderWidth: 2, pointRadius: 4, tension: 0.4 },
          { label: 'Upper Bound', data: result.upperBound,  borderColor: 'rgba(26,115,232,0.3)', borderWidth: 1, pointRadius: 0, tension: 0.4 },
          { label: 'Lower Bound', data: result.lowerBound,  borderColor: 'rgba(26,115,232,0.3)', borderWidth: 1, pointRadius: 0, tension: 0.4 }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'top' } },
        scales:  { x: { grid: { color: '#f1f3f4' } }, y: { grid: { color: '#f1f3f4' } } }
      }
    });
  }
}