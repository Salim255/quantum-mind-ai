import { BlockDTO } from './block.dto';


export interface SectionWithBlocksDTO {

    id: string;

    title: string;

    slug: string;

    description: string;

    order_index: number;

    topic_id: string;

    created_at: string;

    updated_at: string;

    blocks: BlockDTO[];
}
