import { TestBed } from '@angular/core/testing';

import { DetectService } from './detect.service';

describe('DetectService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DetectService = TestBed.get(DetectService);
    expect(service).toBeTruthy();
  });
});
