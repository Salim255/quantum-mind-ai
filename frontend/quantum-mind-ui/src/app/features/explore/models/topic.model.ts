// topic.model.ts

export interface Topic {
  id: string;
  title: string;
  slug: string;
  category: string;
  display_order: number;
  description: string;
}