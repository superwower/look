import { Injectable } from "@angular/core";
import { of, Observable } from "rxjs";

type UserOutput = {
  name: string;
  error?: string;
};

@Injectable({
  providedIn: "root"
})
export class AuthService {
  constructor() {}

  authenticate(data: string): Observable<UserOutput> {
    if (Math.random() < 0.5) {
      // TODO: call http endpoint
      return of({
        name: "hitoshi"
      });
    }
    return of({
      name: "",
      error: "Failed to authenticate"
    });
  }
}
