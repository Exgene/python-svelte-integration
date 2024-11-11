<script lang="ts">
	import { cn } from '$lib/utils';

	let { className = '', title = '', description = '' } = $props();
</script>

<div class={cn('text-left', className)}>
	<h3 class="mb-1 text-lg font-bold text-gray-900 dark:text-gray-100">
		{title}
	</h3>
	<p class="text-gray-700 dark:text-gray-400 font-bold">
		{description}
	</p>
</div>
