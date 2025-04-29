import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { PetCareService } from '../pet-care.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user',
  standalone: true,
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css'],
  imports: [CommonModule, ReactiveFormsModule]
})
export class UserComponent implements OnInit {
  userProfileForm!: FormGroup;

  constructor(private router: Router, private petCareService: PetCareService) {}

  ngOnInit(): void {
    this.userProfileForm = new FormGroup({
      first_name: new FormControl('', Validators.required),
      last_name: new FormControl('', Validators.required),
      email: new FormControl({ value: '', disabled: true }, [Validators.required, Validators.email]),
      phone: new FormControl('', Validators.required),
      address: new FormControl('', Validators.required),
    });

    this.loadUserProfile();
  }

  loadUserProfile(): void {
    this.petCareService.getUserProfile().subscribe({
      next: (profile: any) => {
        if (profile) {
          this.userProfileForm.patchValue({
            first_name: profile.first_name,
            last_name: profile.last_name,
            email: profile.email,
            phone: profile.phone,
            address: profile.address,
          });
        }
      },
      error: (error: any) => {
        console.error('Error retrieving user profile: ', error);
      }
    });
  }

  onUpdate(): void {
    if (this.userProfileForm.valid) {
      const updatedProfile = {
        first_name: this.userProfileForm.value.first_name,
        last_name: this.userProfileForm.value.last_name,
        email: this.userProfileForm.value.email,
        phone: this.userProfileForm.value.phone,
        address: this.userProfileForm.value.address,
      };

      this.petCareService.updateUserProfile(updatedProfile).subscribe({
        next: (response) => {
          console.log('Profile updated successfully!', response);
        },
        error: (error: any) => {
          console.error('Error updating profile:', error);
        }
      })
    }
  }
}
