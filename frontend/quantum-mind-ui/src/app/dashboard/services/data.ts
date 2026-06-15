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
            path: '/linear-Algebra',
          },
           {
            name: 'Complex Numbers versus Real Numbers',
            path: '/complex-versus-vs-real-numbers',
          },
           {
            name: 'Vectors',
            path: '/vectors',
          },
           {
            name: 'Diagrams of Vectors',
            path: '/diagrams-of-vectors',
          },
          {
            name: 'Lengths of Vectors',
            path: '/lengths-of-Vectors',
          },
          {
            name: 'Scalar Multiplication',
            path: '/scalar-multiplication',
          },
          {
            name: 'Vector Addition',
            path: '/vector-Addition',
          },
          {
            name: 'Orthogonal Vectors',
            path: '/orthogonal-vectors',
          },
          {
            name: 'Multiplying a Bra by a Ket',
            path: '/m-bra-Ket',
          },
          {
            name: 'Bra-kets and Lengths',
            path: '/bra-kets-lengths',
          },
          {
            name: 'Bra-kets and Orthogonality',
            path: '/bra-kets-orthogonality',
          },
          {
            name: 'Orthonormal Bases',
            path: '/orthonormal-bases',
          },
          {
            name: 'Vectors as Linear Combinations of Basis Vectors',
            path: '/vectors-li-co-of-ba-vectors',
          },
          {
            name: 'Ordered Bases',
            path: '/ordered-bases',
          },
          {
            name: 'Length of Vectors',
            path: '/length-of-Vectors',
          },
          {
            name: 'Matrices',
            path: '/matrices',
          },
          {
            name: 'Matrix Computations',
            path: '/matrix-computations',
          },
          {
            name: 'Orthogonal and Unitary Matrices',
            path: '/or-and-uni-ma',
          },
          {
            name: 'Linear Algebra Toolbox',
            path: '/linear-algebra-toolbox',
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
