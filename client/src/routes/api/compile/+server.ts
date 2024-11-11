import type { RequestHandler } from '@sveltejs/kit';
import { json } from '@sveltejs/kit';
import { compile } from 'mdsvex';

export const POST: RequestHandler = async ({ request }) => {
	try {
		const { data } = await request.json();

		const result = await compile(data);
		console.log(result?.code);
		return json({
			success: true,
			result: result?.code
		});
	} catch (error) {
		console.error('Compilation error:', error);
		return json(
			{
				success: false,
				error: 'Internal server error'
			},
			{ status: 500 }
		);
	}
};
