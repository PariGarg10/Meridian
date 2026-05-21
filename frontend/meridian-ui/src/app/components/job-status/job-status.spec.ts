import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobStatus } from './job-status';

describe('JobStatus', () => {
  let component: JobStatus;
  let fixture: ComponentFixture<JobStatus>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobStatus],
    }).compileComponents();

    fixture = TestBed.createComponent(JobStatus);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
