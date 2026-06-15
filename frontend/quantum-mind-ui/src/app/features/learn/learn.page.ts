import { Component, OnDestroy, OnInit } from "@angular/core";
import { ContentService } from "./services/content.service";

@Component({
  selector: "app-learn-page",
  templateUrl: "./learn.page.html",
  styleUrls: ["./learn.page.scss"],
  standalone: false
})
export class LearnPage implements OnInit, OnDestroy{

  constructor(private contentService: ContentService){}

  ngOnInit(): void {

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

    ngOnDestroy(): void {
      this.contentService.clearStorage()
    }
}
