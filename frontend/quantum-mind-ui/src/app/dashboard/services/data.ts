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
        name: 'Spin',
        path: '/learn/spin',
      },
      {
        name: 'Linear Algebra',
        path: '/learn/linear-algebra',
      },
      {
        name: 'Spin and Qubits',
        path: '/learn/spin-qubits'
      },
      {
        name: 'Entanglement',
        path: '/learn/entanglement'
      },
      {
        name: 'Bell’s Inequality',
        path: '/learn/bell-Inequality'
      },
      {
        name: 'Classical Logic',
        path: '/learn/classical-logic'
      },
      {
        name: 'Quantum logic',
        path: '/learn/quantum-logic'
      },
      {
        name: 'Quantum Algorithms',
        path: '/learn/quantum-algos'
      },
      {
        name: 'Quantum Computing Impact',
        path: '/learn/quantum-impact'
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
