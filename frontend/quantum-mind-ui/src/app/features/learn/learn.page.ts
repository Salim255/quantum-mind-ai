import { Component, OnDestroy, OnInit, signal } from "@angular/core";
import { ContentService } from "./services/content.service";
import { EventType, NavigationEnd, Router } from "@angular/router";
import { filter } from "rxjs";

@Component({
  selector: "app-learn-page",
  templateUrl: "./learn.page.html",
  styleUrls: ["./learn.page.scss"],
  standalone: false
})
export class LearnPage implements OnInit, OnDestroy{
  closeAside = signal<boolean>(JSON.parse(localStorage.getItem("asideIsClose") ?? 'false'));

  constructor(
    private router: Router,
    private contentService: ContentService
  ){}

  ngOnInit(): void {
    this.listenToRouter()
  }
  /*   Learn

  For consuming knowledge.

  Dashboard
  Learning Paths
  Topics
  Concepts Library
  Quantum Glossary
  Documentation
  Resources

  Examples:

  Learn
  ├── Learning Paths
  ├── Topics
  ├── Concepts
  ├── Glossary
  ├── Documentation
  └── Resources */
/*
  Learn
├── Mathematics
│   ├── Linear Algebra
│   ├── Complex Numbers
│   ├── Vectors & Matrices
│   ├── Probability
│   └── Tensor Products
│
├── Physics
│   ├── Classical Physics
│   ├── Quantum Mechanics
│   ├── Wave Functions
│   ├── Superposition
│   ├── Entanglement
│   └── Measurement Theory
│
├── Quantum Computing
│   ├── Qubits
│   ├── Quantum Gates
│   ├── Quantum Circuits
│   ├── Quantum Error Correction
│   └── Quantum Hardware
│
├── Quantum Algorithms
│   ├── Deutsch-Jozsa
│   ├── Grover's Algorithm
│   ├── Shor's Algorithm
│   ├── Quantum Fourier Transform
│   └── Variational Algorithms
│
└── Applications
    ├── Cryptography
    ├── Optimization
    ├── Chemistry
    ├── Machine Learning
    └── Finance */

  listenToRouter(): void {
     this.router.events.pipe(
        filter(event => event.type === EventType.NavigationEnd)
      ).subscribe((event: NavigationEnd) => {
          const url =  event.url;
          if (url === '/learn') {
            this.closeAside.set(false);
            localStorage.setItem("asideIsClose", JSON.stringify(false));
          } else {
            this.closeAside.set(true);
            localStorage.setItem("asideIsClose", JSON.stringify(true));
          }
      });
  }
  ngOnDestroy(): void {
    this.contentService.clearStorage()
  }
}
