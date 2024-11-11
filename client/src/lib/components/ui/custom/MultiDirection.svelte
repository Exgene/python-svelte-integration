<script lang="ts">
	// Scroll down to see the original Component
	import { cn } from '$lib/utils';
	import AnimatedBeam from './AnimatedBeam.svelte';
	import Circle from './Circle.svelte';
	let containerRef;
	export let numberOfNodes = 3;
	export let routedNode = 0;
	// Circles

	let div6Ref;
	let div7Ref;

	let divRefs = Array.from({ length: numberOfNodes }, () => null);
	let className: any = '';
	export { className as class };
</script>

<div
	bind:this={containerRef}
	class={cn(
		'bg-background relative flex w-full max-w-[500px] items-center justify-center overflow-hidden rounded-lg border p-10  md:shadow-xl dark:shadow-[#090909]',
		className
	)}
>
	<!--  Gradient Line -->
	<div
		class="absolute right-5 top-0 h-px w-1/2 bg-gradient-to-l from-transparent via-white/30 via-10% to-transparent"
	></div>
	<!-- Main Component  -->

	<div class="flex h-full w-full max-w-lg flex-row items-center justify-between gap-10 text-white">
		<div class="flex flex-col justify-center">
			<div class="absolute bottom-16 left-4 text-sm text-slate-500">Input Prompts</div>
			<!-- Div 7 -->
			<Circle>
				<svg
					bind:this={div7Ref}
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					stroke="#ffffff"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="lucide lucide-network"
				>
					<rect x="16" y="16" width="6" height="6" rx="1" />
					<rect x="2" y="16" width="6" height="6" rx="1" />
					<rect x="9" y="2" width="6" height="6" rx="1" />
					<path d="M5 16v-4h14v4" />
					<path d="M12 12V8" />
				</svg>
			</Circle>
		</div>
		<div class="relative flex flex-col justify-center">
			<!-- Div 6 -->
			<div class="absolute -bottom-8 left-1 text-sm text-slate-500">Router</div>

			<Circle>
				<svg
					bind:this={div6Ref}
					xmlns="http://www.w3.org/2000/svg"
					width="40"
					height="40"
					viewBox="0 0 24 24"
					fill="none"
					stroke="#4F46E5"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<path d="M5 12.55a11 11 0 0 1 14.08 0" />
					<path d="M1.42 9a16 16 0 0 1 21.16 0" />
					<path d="M8.53 16.11a6 6 0 0 1 6.95 0" />
					<line x1="12" y1="20" x2="12" y2="20" />
				</svg>
			</Circle>
		</div>
		<div class="flex flex-col justify-center gap-2 text-sm text-white">
			{#each divRefs as divRef, i}
				<!-- Div {i + 1} -->
				<Circle class="relative">
					<div class="absolute -right-4 text-slate-500">{i + 1}</div>
					<svg
						bind:this={divRef}
						viewBox="0 0 24 24"
						width="40"
						height="40"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						stroke="#4F46E5"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<rect x="2" y="2" width="20" height="20" rx="2" ry="2" />
						<circle cx="12" cy="12" r="4" />
						<text
							x="12"
							y="12"
							text-anchor="middle"
							dy=".3em"
							fill="#4F46E5"
							stroke="none"
							font-size="8">{i + 1}</text
						>
					</svg>
				</Circle>
			{/each}
		</div>
	</div>
	{#each divRefs as divRef, i}
		<AnimatedBeam
			bind:containerRef
			bind:fromRef={divRef}
			bind:toRef={div6Ref}
			correctPath={routedNode === i + 1 ? 1 : 0}
		/>
	{/each}
	<AnimatedBeam bind:containerRef bind:fromRef={div6Ref} bind:toRef={div7Ref} correctPath={1} />
</div>
