import { NavItem } from "./aside-nav.service";

export const NAVIGATION: NavItem[] = [
  {
    name: 'Home',
    path: '/home',
    children: [
      {
        name: 'Home',
        path: '/home',
      },
      {
        name: 'Learn',
        path: '/learn'
      },
      {
        name: 'Practice',
        path: '/practice'
      },
      {
        name: 'Progress',
        path: '/progress'
      },
      {
        name: 'Explore',
        path: '/explore '
      }
    ]
  },

  {
    name: 'Learn',
    path: '/learn',
    children: [
      {
        name: 'Mathematics',
        path: '/learn/mathematics',
        children: [
          {
            name: 'Linear Algebra',
            path: '/learn/mathematics/linear-Algebra',
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
      },
      {
        name: 'Physics',
        path: '/learn/physics'
      },
      {
        name: 'Quantum Computing',
        path: '/learn/quantum-computing'
      },
      {
        name: 'Algorithms',
        path: '/learn/algorithms'
      }
    ]
  },

  {
    name: 'Practice',
    path: '/practice',
    children: [
      {
        name: 'Quizzes',
        path: '/practice/quizzes'
      },
      {
        name: 'Exercises',
        path: '/practice/exercises'
      }
    ]
  },

  {
    name: 'Progress',
    path: '/progress',
    children: [
      {
        name: 'Analytics',
        path: '/progress/analytics'
      }
    ]
  },

  {
    name: 'Resources',
    path: '/resources',
    children: [
      {
        name: 'Documentation',
        path: '/resources/docs'
      },
      {
        name: 'Glossary',
        path: '/resources/glossary'
      }
    ]
  }
];
