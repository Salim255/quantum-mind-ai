import { BELL_INEQUALITY, CLASSICAL_LOGIC, ENTANGLEMENT, LINEAR_ALGEBRA, QUANTUM_ALGOS, QUANTUM_IMPACT, QUANTUM_LOGIC, SPIN, SPIN_QUBITS } from "../../features/learn/services/data";
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
        sections: SPIN
      },
      {
        name: 'Linear Algebra',
        path: '/learn/linear-algebra',
        sections: LINEAR_ALGEBRA
      },
      {
        name: 'Spin and Qubits',
        path: '/learn/spin-qubits',
        sections: SPIN_QUBITS
      },
      {
        name: 'Entanglement',
        path: '/learn/entanglement',
        sections: ENTANGLEMENT
      },
      {
        name: 'Bell’s Inequality',
        path: '/learn/bell-Inequality',
        sections: BELL_INEQUALITY
      },
      {
        name: 'Classical Logic',
        path: '/learn/classical-logic',
        sections: CLASSICAL_LOGIC
      },
      {
        name: 'Quantum logic',
        path: '/learn/quantum-logic',
        sections: QUANTUM_LOGIC,
      },
      {
        name: 'Quantum Algorithms',
        path: '/learn/quantum-algos',
        sections: QUANTUM_ALGOS
      },
      {
        name: 'Quantum Computing Impact',
        path: '/learn/quantum-impact',
        sections: QUANTUM_IMPACT
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
