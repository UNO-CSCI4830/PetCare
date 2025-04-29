import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { PetCareService } from '../pet-care.service';

type User = {
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
}

@Component({
  selector: 'app-sign-in',
  standalone: false,
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent implements OnInit {
  userExists = false;

  constructor(private router:Router, private petCareService: PetCareService){}

  loginForm!: FormGroup;

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      email: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
    })
   
  }

  onSubmit(){
    const credentials = this.loginForm.value;
    console.log("credentials: ", credentials);

    this.petCareService.login(credentials).subscribe({
      next: (response) => {
        console.log("Response from login: ", response);
        if(response) {
          this.goToMainDashboard();
        }
      
      }
    })


  }

  goToSignUp(){
    this.router.navigate(['sign-up']);
  }

  goToMainDashboard(){
    this.router.navigate(['main-dashboard']);
  }

  checkExistentUsers(object: Object) {
    this.petCareService.login(object).subscribe({
      next: (response) => {
        console.log("Response from login: ", response);
        
      
      }
    })
  }


}
