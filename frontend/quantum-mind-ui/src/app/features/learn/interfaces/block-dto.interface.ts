export type BlockType =
  | 'paragraph'
  | 'heading'
  | 'image'
  | 'code'
  | 'equation';


export interface BlockDTO {
    id: string;

    type: BlockType;

    content: string;

    display_order: number;

    topic_id: string | null;

    section_id: string | null;

    created_at: string;

    updated_at: string;
}
