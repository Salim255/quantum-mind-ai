import { Component, signal } from "@angular/core";
import { AssistantMessage } from "../assistant-message/assistant-message.component";

export interface AssistantConversation {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}

@Component({
  selector: "app-assistant-conversation",
  templateUrl: "./assistant-conversation.component.html",
  styleUrl: "./assistant-conversation.component.scss",
  standalone: false
})
export class AssistantConversationComponent {
 ASSISTANT_MESSAGES: AssistantMessage[] = [
  {
    id: "msg-001",
    conversationId: "conversation-001",
    role: "user",
    content: "What is quantum entanglement?",
    createdAt: new Date("2026-08-13T09:00:00")
  },
  {
    id: "msg-002",
    conversationId: "conversation-001",
    role: "assistant",
    content:
      "Quantum entanglement is a physical phenomenon where two or more quantum systems become correlated in such a way that their states cannot be described independently. Measuring one system can reveal information about the other, even when they are separated by a large distance.\n\nImportantly, entanglement does not allow information to travel faster than light. The correlations are established by the shared quantum state, while usable classical communication is still limited by the speed of light.",
    createdAt: new Date("2026-08-13T09:00:08")
  },
  {
    id: "msg-003",
    conversationId: "conversation-001",
    role: "user",
    content: "Can you explain that in simpler terms?",
    createdAt: new Date("2026-08-13T09:01:00")
  },
  {
    id: "msg-004",
    conversationId: "conversation-001",
    role: "assistant",
    content:
      "Think of two particles as having a shared quantum relationship.\n\nBefore you measure them, their individual states are not fully determined. Once you measure one particle, you immediately know what result you will get when measuring the other in the corresponding basis.\n\nThe surprising part is that this relationship remains even when the particles are very far apart.",
    createdAt: new Date("2026-08-13T09:01:07")
  },
  {
    id: "msg-005",
    conversationId: "conversation-001",
    role: "user",
    content: "Does that mean they communicate instantly?",
    createdAt: new Date("2026-08-13T09:02:00")
  },
  {
    id: "msg-006",
    conversationId: "conversation-001",
    role: "assistant",
    content:
      "No. This is one of the most important distinctions in quantum mechanics.\n\nThe measurement outcomes are correlated, but you cannot control the outcome of the first measurement in a way that lets you encode and transmit a message to the second particle.\n\nTherefore, entanglement produces correlations that are stronger than classical physics allows, but it does not provide faster-than-light communication.",
    createdAt: new Date("2026-08-13T09:02:09")
  },
  {
    id: "msg-007",
    conversationId: "conversation-001",
    role: "user",
    content: "What is a qubit then?",
    createdAt: new Date("2026-08-13T09:03:00")
  },
  {
    id: "msg-008",
    conversationId: "conversation-001",
    role: "assistant",
    content:
      "A qubit is the basic unit of quantum information.\n\nA classical bit can be either 0 or 1. A qubit can exist in a quantum superposition of the states |0⟩ and |1⟩. Mathematically, its state can be written as:\n\n|ψ⟩ = α|0⟩ + β|1⟩\n\nwhere α and β are complex amplitudes whose squared magnitudes determine the probabilities of measuring 0 or 1.",
    createdAt: new Date("2026-08-13T09:03:12")
  },
  {
    id: "msg-009",
    conversationId: "conversation-001",
    role: "user",
    content: "How is a qubit different from a normal bit?",
    createdAt: new Date("2026-08-13T09:04:00")
  },
  {
    id: "msg-010",
    conversationId: "conversation-001",
    role: "assistant",
    content:
      "The key difference is how information is represented.\n\nA classical bit has one definite state at a time: 0 or 1.\n\nA qubit can be in a superposition of both basis states until it is measured. Measurement then produces a classical result, either 0 or 1, according to the probabilities encoded in the quantum state.\n\nQubits can also become entangled with one another, creating correlations that have no direct classical equivalent.",
    createdAt: new Date("2026-08-13T09:04:10")
  },
  {
    id: "msg-011",
    conversationId: "conversation-001",
    role: "user",
    content: "Can you give me a practical example of where quantum computing could be useful?",
    createdAt: new Date("2026-08-13T09:05:00")
  },
  {
    id: "msg-012",
    conversationId: "conversation-001",
    role: "assistant",
    content:
      "One promising area is quantum simulation.\n\nQuantum computers can naturally represent quantum states, which makes them potentially useful for studying molecules, materials, chemical reactions, and other physical systems that become difficult to simulate accurately with classical computers.\n\nOther areas being investigated include optimization, cryptography, and certain search or mathematical problems. However, the practical advantage depends heavily on the specific problem and the quality and scale of the quantum hardware.",
    createdAt: new Date("2026-08-13T09:05:18")
  }
];
  messages = signal<AssistantMessage []>(this.ASSISTANT_MESSAGES)
}
