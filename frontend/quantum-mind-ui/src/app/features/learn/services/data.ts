export const SPIN = [
  { id: "quantum-clock", name: "The Quantum Clock" },
  { id: "measurements-in-same-direction", name: "Measurements in the Same Direction" },
  { id: "measurements-different-directions", name: "Measurements in Different Directions" },
  { id: "measurements", name: "Measurements" },
  { id: "randomness", name: "Randomness" },
  { id: "photons-and-polarization", name: "Photons and Polarization" }
];


export const LINEAR_ALGEBRA = [
  { id: "complex-numbers-versus-real-numbers", name: "Complex Numbers versus Real Numbers" },
  { id: "vectors", name: "Vectors" },
  { id: "diagrams-of-vectors", name: "Diagrams of Vectors" },
  { id: "lengths-of-vectors", name: "Lengths of Vectors" },
  { id: "scalar-multiplication", name: "Scalar Multiplication" },
  { id: "vector-addition", name: "Vector Addition" },
  { id: "orthogonal-vectors", name: "Orthogonal Vectors" },
  { id: "multiplying-bra-by-ket", name: "Multiplying a Bra by a Ket" },
  { id: "bra-kets-and-lengths", name: "Bra-kets and Lengths" },
  { id: "bra-kets-and-orthogonality", name: "Bra-kets and Orthogonality" },
  { id: "orthonormal-bases", name: "Orthonormal Bases" },
  { id: "vectors-as-linear-combinations", name: "Vectors as Linear Combinations of Basis Vectors" },
  { id: "ordered-bases", name: "Ordered Bases" },
  { id: "length-of-vectors", name: "Length of Vectors" },
  { id: "matrices", name: "Matrices" },
  { id: "matrix-computations", name: "Matrix Computations" },
  { id: "orthogonal-and-unitary-matrices", name: "Orthogonal and Unitary Matrices" },
  { id: "linear-algebra-toolbox", name: "Linear Algebra Toolbox" }
];


// 3 Spin and Qubits
export const SPIN_QUBITS = [
  { id: "probability", name: "Probability" },
  { id: "mathematics-of-quantum-spin", name: "Mathematics of Quantum Spin" },
  { id: "equivalent-state-vectors", name: "Equivalent State Vectors" },
  { id: "basis-for-spin-direction", name: "The Basis Associated with a Given Spin Direction" },
  { id: "rotating-apparatus-60", name: "Rotating the Apparatus through 60°" },
  { id: "model-for-photon-polarization", name: "The Mathematical Model for Photon Polarization" },
  { id: "basis-for-polarization-direction", name: "The Basis Associated with a Given Polarization Direction" },
  { id: "polarized-filters-experiments", name: "The Polarized Filters Experiments" },
  { id: "qubits", name: "Qubits" },
  { id: "alice-bob-eve", name: "Alice, Bob, and Eve" },
  { id: "probability-amplitudes-interference", name: "Probability Amplitudes and Interference" },
  { id: "bb84-protocol", name: "Alice, Bob, Eve, and the BB84 Protocol" },
  { id: "model-for-photon-polarization-2", name: "The Mathematical Model for Photon Polarization" }
];


/// 4 Entanglement
export const ENTANGLEMENT = [
  { id: "alice-bob-not-entangled", name: "Alice and Bob’s Qubits Are Not Entangled" },
  { id: "unentangled-qubits-calculation", name: "Unentangled Qubits Calculation" },
  { id: "entangled-qubits-calculation", name: "Entangled Qubits Calculation" },
  { id: "superluminal-communication", name: "Superluminal Communication" },
  { id: "standard-basis-tensor-products", name: "The Standard Basis for Tensor Products" },
  { id: "how-to-entangle-qubits", name: "How Do You Entangle Qubits?" },
  { id: "cnot-gate-entanglement", name: "Using the CNOT Gate to Entangle Qubits" },
  { id: "entangled-quantum-clocks", name: "Entangled Quantum Clocks" }
];


// Bell’s Inequality
export const BELL_INEQUALITY = [
  { id: "entangled-qubits-different-bases", name: "Entangled Qubits in Different Bases" },
  { id: "einstein-local-realism", name: "Einstein and Local Realism" },
  { id: "einstein-hidden-variables", name: "Einstein and Hidden Variables" },
  { id: "classical-explanation-entanglement", name: "A Classical Explanation of Entanglement" },
  { id: "bells-inequality", name: "Bell’s Inequality" },
  { id: "quantum-mechanics-answer", name: "The Answer of Quantum Mechanics" },
  { id: "classical-answer", name: "The Classical Answer" },
  { id: "measurement", name: "Measurement" },
  { id: "ekert-protocol", name: "The Ekert Protocol for Quantum Key Distribution" }
];


// 6 Classical Logic, Gates, and Circuits
export const CLASSICAL_LOGIC = [
  { id: "logic", name: "Logic" },
  { id: "boolean-algebra", name: "Boolean Algebra" },
  { id: "functional-completeness", name: "Functional Completeness" },
  { id: "gates", name: "Gates" },
  { id: "circuits", name: "Circuits" },
  { id: "nand-universal-gate", name: "NAND Is a Universal Gate" },
  { id: "gates-and-computation", name: "Gates and Computation" },
  { id: "memory", name: "Memory" },
  { id: "reversible-computation", name: "Reversible Computation" },
  { id: "billiard-ball-computing", name: "Billiard Ball Computing" }
];


// 7 Quantum Gates and Circuits
export const QUANTUM_LOGIC = [
  { id: "qubits", name: "Qubits" },
  { id: "cnot-gate", name: "The CNOT Gate" },
  { id: "quantum-gates", name: "Quantum Gates" },
  { id: "quantum-gates-one-qubit", name: "Quantum Gates Acting on One Qubit" },
  { id: "universal-quantum-gates", name: "Are There Universal Quantum Gates?" },
  { id: "no-cloning-theorem", name: "No Cloning Theorem" },
  { id: "quantum-vs-classical-computation", name: "Quantum Computation versus Classical Computation" },
  { id: "bell-circuit", name: "The Bell Circuit" },
  { id: "superdense-coding", name: "Superdense Coding" },
  { id: "quantum-teleportation", name: "Quantum Teleportation" },
  { id: "error-correction", name: "Error Correction" }
];

// 8 Quantum Algorithms
export const QUANTUM_ALGOS = [
  { id: "complexity-classes-p-np", name: "The Complexity Classes P and NP" },
  { id: "quantum-vs-classical-speed", name: "Are Quantum Algorithms Faster Than Classical Ones?" },
  { id: "query-complexity", name: "Query Complexity" },
  { id: "deutsch-algorithm", name: "Deutsch’s Algorithm" },
  { id: "kronecker-hadamard", name: "The Kronecker Product of Hadamard Matrices" },
  { id: "deutsch-jozsa", name: "The Deutsch-Jozsa Algorithm" },
  { id: "simon-algorithm", name: "Simon’s Algorithm" },
  { id: "complexity-classes", name: "Complexity Classes" },
  { id: "quantum-algorithms", name: "Quantum Algorithms" }
];

//9 Impact of Quantum Computing
export const QUANTUM_IMPACT = [
  { id: "shor-algorithm-cryptanalysis", name: "Shor’s Algorithm and Cryptanalysis" },
  { id: "grover-algorithm-searching", name: "Grover’s Algorithm and Searching Data" },
  { id: "chemistry-simulation", name: "Chemistry and Simulation" },
  { id: "hardware", name: "Hardware" },
  { id: "quantum-supremacy-parallel-universes", name: "Quantum Supremacy and Parallel Universes" },
  { id: "computation", name: "Computation" }
];

