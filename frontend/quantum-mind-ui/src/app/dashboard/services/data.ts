import { BELL_INEQUALITY, CLASSICAL_LOGIC, ENTANGLEMENT, LINEAR_ALGEBRA, QUANTUM_ALGOS, QUANTUM_IMPACT, QUANTUM_LOGIC, SPIN, SPIN_QUBITS } from "../../features/learn/services/data";
import { NavItem } from "./aside-nav.service";

export const NAVIGATION: NavItem[] = [
  {
    id: 'home',
    name: 'Home',
    path: '/home',
    icon: 'lucide:house',
    children: [
      {
        id: 'overview',
        name: 'Overview',
        path: '/home',
        icon: 'lucide:layout-dashboard'
      },
      {
        id: 'learn',
        name: 'Learn',
        path: '/learn',
        icon: 'lucide:graduation-cap'
      },
      {
        id: 'practice',
        name: 'Practice',
        path: '/practice',
        icon: 'lucide:square-check-big'
      },
      {
        id: 'progress',
        name: 'Progress',
        path: '/progress',
        icon: 'lucide:chart-column'
      },
      {
        id: 'explore',
        name: 'Explore',
        path: '/explore',
        icon: 'lucide:compass'
      }
    ]
  },

  {
    id: 'learn',
    name: 'Learn',
    path: '/learn',
    icon: 'lucide:graduation-cap',
    children: [
      {
        id: 'spin',
        name: 'Spin',
        path: '/learn/spin',
        icon: 'lucide:atom',
        sections: SPIN
      },
      {
        id: 'linear-algebra',
        name: 'Linear Algebra',
        path: '/learn/linear-algebra',
        icon: 'lucide:sigma',
        sections: LINEAR_ALGEBRA
      },
      {
        id: 'spin-qubits',
        name: 'Spin and Qubits',
        path: '/learn/spin-qubits',
        icon: 'lucide:orbit',
        sections: SPIN_QUBITS
      },
      {
        id: 'entanglement',
        name: 'Entanglement',
        path: '/learn/entanglement',
        icon: 'lucide:git-merge',
        sections: ENTANGLEMENT
      },
      {
        id: 'bell-inequality',
        name: 'Bell’s Inequality',
        path: '/learn/bell-inequality',
        icon: 'lucide:waypoints',
        sections: BELL_INEQUALITY
      },
      {
        id: 'classical-logic',
        name: 'Classical Logic',
        path: '/learn/classical-logic',
        icon: 'lucide:binary',
        sections: CLASSICAL_LOGIC
      },
      {
        id: 'quantum-logic',
        name: 'Quantum Logic',
        path: '/learn/quantum-logic',
        icon: 'lucide:cpu',
        sections: QUANTUM_LOGIC
      },
      {
        id: 'quantum-algorithms',
        name: 'Quantum Algorithms',
        path: '/learn/quantum-algos',
        icon: 'lucide:brain-circuit',
        sections: QUANTUM_ALGOS
      },
      {
        id: 'quantum-impact',
        name: 'Quantum Computing Impact',
        path: '/learn/quantum-impact',
        icon: 'lucide:sparkles',
        sections: QUANTUM_IMPACT
      }
    ]
  },

  {
    id: 'practice',
    name: 'Practice',
    path: '/practice',
    icon: 'lucide:square-check-big',
    children: [
      {
        id: 'quizzes',
        name: 'Quizzes',
        path: '/practice/quizzes',
        icon: 'lucide:clipboard-check'
      },
      {
        id: 'exercises',
        name: 'Exercises',
        path: '/practice/exercises',
        icon: 'lucide:dumbbell'
      }
    ]
  },

  {
    id: 'progress',
    name: 'Progress',
    path: '/progress',
    icon: 'lucide:chart-column',
    children: [
      {
        id: 'analytics',
        name: 'Analytics',
        path: '/progress/analytics',
        icon: 'lucide:chart-line'
      }
    ]
  },

  {
    id: 'resources',
    name: 'Resources',
    path: '/resources',
    icon: 'lucide:book-open',
    children: [
      {
        id: 'documentation',
        name: 'Documentation',
        path: '/resources/docs',
        icon: 'lucide:file-text'
      },
      {
        id: 'glossary',
        name: 'Glossary',
        path: '/resources/glossary',
        icon: 'lucide:book-text'
      }
    ]
  }
];
