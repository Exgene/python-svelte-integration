<script lang="ts">
	import { cn } from '$lib/utils';

	type Direction = 'top' | 'bottom';

	let { direction = 'bottom', className = '' }: { direction: Direction; className: string } =
		$props();
</script>

<div class={cn('h-full w-full overflow-hidden', className)}>
	<div
		style={`background: conic-gradient(from 0deg at 50% 50%, var(--blue-500) 0deg, var(--cyan-400) 180deg, var(--yellow-400) 1turn); filter: blur(75px); opacity: 20%;`}
		class={`relative bottom-[500px] h-full w-full`}
	></div>
</div>
