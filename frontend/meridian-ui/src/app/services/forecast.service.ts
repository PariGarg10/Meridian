import { Injectable }    from '@angular/core';
import { HttpClient }    from '@angular/common/http';
import { Observable, interval, switchMap, takeWhile } from 'rxjs';

export interface ForecastRequest {
  tenantId:    string;
  datasetRef:  string;
  horizonDays: number;
}

export interface JobResponse {
  jobId:  string;
  status: string;
}

export interface ForecastResult {
  jobId:       string;
  modelUsed:   string;
  dates:       string[];
  predictions: number[];
  upperBound:  number[];
  lowerBound:  number[];
  allScores:   { prophet: number; arima: number; lstm: number };
}

@Injectable({ providedIn: 'root' })
export class ForecastService {

  // Points to our Python REST bridge (we add this in a moment)
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  submitJob(request: ForecastRequest): Observable<JobResponse> {
    return this.http.post<JobResponse>(`${this.baseUrl}/forecast`, request);
  }

  getJobStatus(jobId: string): Observable<JobResponse> {
    return this.http.get<JobResponse>(`${this.baseUrl}/status/${jobId}`);
  }

  getResult(jobId: string): Observable<ForecastResult> {
    return this.http.get<ForecastResult>(`${this.baseUrl}/result/${jobId}`);
  }

  // Poll job status every 3 seconds until DONE or FAILED
  pollUntilDone(jobId: string): Observable<JobResponse> {
    return interval(3000).pipe(
      switchMap(() => this.getJobStatus(jobId)),
      takeWhile(r => r.status === 'PENDING' || r.status === 'RUNNING', true)
    );
  }
}