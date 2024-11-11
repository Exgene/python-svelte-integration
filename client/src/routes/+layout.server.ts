import type { Actions } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ fetch }) => {
    const data = await import('$lib/config/nodes.json')
    
    return {
        nodes: JSON.parse(JSON.stringify(data))
    };
};
