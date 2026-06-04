import { NavItem } from "./aside-nav.service";

export const NAVIGATION: NavItem[] = [
  {
    name: 'Home',
    path: '/home',
    children: [
      {
        name: 'Overview',
        path: '/home/overview'
      },
      {
        name: 'Getting Started',
        path: '/home/getting-started'
      }
    ]
  },

  {
    name: 'Learn',
    path: '/learn',
    children: [
      {
        name: 'Mathematics',
        path: '/learn/mathematics'
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
