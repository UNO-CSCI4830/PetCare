import { TestBed } from '@angular/core/testing';
import { HttpTestingController } from '@angular/common/http/testing';
import { PetCareService } from './pet-care.service';
import { provideHttpClient } from '@angular/common/http';

type User = {
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
}

type Pet = {
  age: string;
  breed: string;
  gender: string;
  name: string;
  owners: any[];
  pet_id: number;
  profile_picture: any;
  species: string;
  weight: string;
}

type Vaccinations = {
  created_at: string;
  date_given: string;
  next_due: string; 
  pet_id: number;
  vaccination_id: number;
  vaccine_name: string;
  veterinarian_id: number;
  veterinarian_name: string;
}

type Medication = {
  created_at: string;
  dosage: string;
  end_date: string;
  frequency: string;
  medication_id: number;
  medication_name: string;
  pet_id: number;
  prescribed_by: string;
  start_date: string;
} 

describe('PetCareService', () => {
  let service: PetCareService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [PetCareService],
      imports: [provideHttpClient]
    });
    service = TestBed.inject(PetCareService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch pets', () => {
    const mockPets: Pet[] = [
      { age: '2', breed: 'Labrador', gender: 'Male', name: 'Buddy', owners: [], pet_id: 1, profile_picture: null, species: 'Dog', weight: '30kg' },
      { age: '3', breed: 'Beagle', gender: 'Female', name: 'Max', owners: [], pet_id: 2, profile_picture: null, species: 'Dog', weight: '25kg' }
    ];

    service.getPets().subscribe(pets => {
      expect(pets).toEqual(mockPets);
    });

    const req = httpMock.expectOne('http://localhost:5001/pets/4');
    expect(req.request.method).toBe('GET');
    req.flush(mockPets);
  });

  it('should login user', () => {
    const mockCredentials = { username: 'test', password: 'test' };
    const mockResponse: User = { email: 'test@example.com', first_name: 'Test', last_name: 'User', phone: '1234567890' };

    service.login(mockCredentials).subscribe(response => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne('http://localhost:5001/users/login');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(mockCredentials);
    req.flush(mockResponse);
  });

  it('should fetch user profile', () => {
    const mockUser: User = {
      email: 'john@example.com',
      first_name: 'John',
      last_name: 'Doe',
      phone: '555-5555'
    };

    service.getUserProfile().subscribe(user => {
      expect(user).toEqual(mockUser);
    });

    const req = httpMock.expectOne('http://localhost:5001/user-profile');
    expect(req.request.method).toBe('GET');
    req.flush(mockUser);
  });

  it('should update user profile', () => {
    const updatedUser: User = {
      email: 'john@example.com',
      first_name: 'Johnny',
      last_name: 'Doe',
      phone: '555-1234'
    };

    service.updateUserProfile(updatedUser).subscribe(response => {
      expect(response).toEqual(updatedUser);
    });

    const req = httpMock.expectOne('http://localhost:5001/user-profile');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(updatedUser);
    req.flush(updatedUser);
  });

  it('should fetch medications', () => {
    const mockMedications: Medication[] = [
      {
        created_at: '2023-01-01',
        dosage: '1 tablet',
        end_date: '2023-01-10',
        frequency: 'Once a day',
        medication_id: 1,
        medication_name: 'Medication A',
        pet_id: 1,
        prescribed_by: 'Dr. Smith',
        start_date: '2023-01-01'
      }
    ];

    service.getMedications().subscribe(medications => {
      expect(medications).toEqual(mockMedications);
    });

    const req = httpMock.expectOne('http://localhost:5001/medications/1');
    expect(req.request.method).toBe('GET');
    req.flush(mockMedications);
  });

  it('should fetch vaccinations', () => {
    const mockVaccinations: Vaccinations[] = [
      {
        created_at: '2023-02-01',
        date_given: '2023-02-01',
        next_due: '2024-02-01',
        pet_id: 2,
        vaccination_id: 1,
        vaccine_name: 'Rabies',
        veterinarian_id: 100,
        veterinarian_name: 'Dr. Jane'
      }
    ];

    service.fetchVaccinations().subscribe(vaccinations => {
      expect(vaccinations).toEqual(mockVaccinations);
    });

    const req = httpMock.expectOne('http://localhost:5001/vaccinations/pet/2');
    expect(req.request.method).toBe('GET');
    req.flush(mockVaccinations);
  });
});
