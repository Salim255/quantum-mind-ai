import { BlockDTO } from './block.dto';
import { SectionWithBlocksDTO } from './section-with-blocks.dto';


export interface TopicWithSectionsDTO {

    id: string;

    title: string;

    slug: string;

    category: string;

    display_order: number;

    description: string;

    created_at: string;

    updated_at: string;


    /**
     * Blocks directly attached to the topic.
     */
    blocks: BlockDTO[];


    /**
     * Sections belonging to this topic.
     */
    sections: SectionWithBlocksDTO[];
}
