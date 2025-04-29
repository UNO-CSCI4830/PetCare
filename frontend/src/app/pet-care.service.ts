import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PetCareService {

  constructor( private http: HttpClient) { }

  baseUrl = "http://localhost:5001";

  getPets(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/pets/${4}`);
  }

  login(credentials: Object): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/users/login`, credentials);
  }

  getUserProfile(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/user-profile`);
  }

  updateUserProfile(profile: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/user-profile`, profile);
  }

  getMedications(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/medications/${1}`);
  }

  fetchAppointments(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/appointments`);
  }

  fetchVaccinations(): Observable<any>{
    return this.http.get<any>(`${this.baseUrl}/vaccinations/pet/${2}`);
  }

}
