import { Component, OnInit } from "@angular/core";

@Component({
  selector: "app-content-aside",
  templateUrl: "./page-content-aside.component.html",
  styleUrl: "./page-content-aside.component.scss",
  standalone: false
})
export class PageContentAsideComponent implements OnInit {
  list =   [
          {
            name: 'Linear Algebra',
            path: '/learn/mathematics/linear-Algebra'
          },
           {
            name: 'Complex Numbers versus Real Numbers',
            path: '/learn/mathematics/complex-versus-vs-real-numbers',
          },
           {
            name: 'Vectors',
            path: '/learn/mathematics/vectors',
          },
           {
            name: 'Diagrams of Vectors',
            path: '/learn/mathematics/diagrams-of-vectors',
          },
          {
            name: 'Lengths of Vectors',
            path: '/learn/mathematics/lengths-of-Vectors',
          },
          {
            name: 'Scalar Multiplication',
            path: '/learn/mathematics/scalar-multiplication',
          },
          {
            name: 'Vector Addition',
            path: '/learn/mathematics/vector-Addition',
          },
          {
            name: 'Orthogonal Vectors',
            path: '/learn/mathematics/orthogonal-vectors',
          },
          {
            name: 'Multiplying a Bra by a Ket',
            path: '/learn/mathematics/m-bra-Ket',
          },
          {
            name: 'Bra-kets and Lengths',
            path: '/learn/mathematics/bra-kets-lengths',
          },
          {
            name: 'Bra-kets and Orthogonality',
            path: '/learn/mathematics/bra-kets-orthogonality',
          },
          {
            name: 'Orthonormal Bases',
            path: '/learn/mathematics/orthonormal-bases',
          },
          {
            name: 'Vectors as Linear Combinations of Basis Vectors',
            path: '/learn/mathematics/vectors-li-co-of-ba-vectors',
          },
          {
            name: 'Ordered Bases',
            path: '/learn/mathematics/ordered-bases',
          },
          {
            name: 'Length of Vectors',
            path: '/learn/mathematics/length-of-Vectors',
          },
          {
            name: 'Matrices',
            path: '/learn/mathematics/matrices',
          },
          {
            name: 'Matrix Computations',
            path: '/learn/mathematics/matrix-computations',
          },
          {
            name: 'Orthogonal and Unitary Matrices',
            path: '/learn/mathematics/or-and-uni-ma',
          },
          {
            name: 'Linear Algebra Toolbox',
            path: '/learn/mathematics/linear-algebra-toolbox',
          }
        ]
  ngOnInit(): void {

  }
}
