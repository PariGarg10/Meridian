import { Component, OnInit } from '@angular/core';
import { CommonModule }      from '@angular/common';
import { RouterModule }      from '@angular/router';

@Component({
  selector:    'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls:   ['./dashboard.component.scss'],
  standalone:  true,
  imports:     [CommonModule, RouterModule]
})
export class DashboardComponent implements OnInit {

  recentJobs: any[] = [];

  models = [
    { icon: '📈', name: 'Prophet', description: 'Facebook\'s forecasting model. Handles holidays and seasonal patterns automatically.', bestFor: 'Best for: seasonal data' },
    { icon: '📊', name: 'ARIMA',   description: 'Classic statistical model. Fast and reliable for smooth, stable trends.',              bestFor: 'Best for: stable trends' },
    { icon: '🧠', name: 'LSTM',    description: 'Deep learning neural network. Captures complex non-linear patterns.',                  bestFor: 'Best for: complex patterns' }
  ];

  ngOnInit() {
    const saved = localStorage.getItem('meridian_jobs');
    if (saved) this.recentJobs = JSON.parse(saved);
  }
}