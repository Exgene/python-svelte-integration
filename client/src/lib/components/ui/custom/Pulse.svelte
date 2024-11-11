<script lang="ts">
	let { mainCircleSize = 210, mainCircleOpacity = 0.2, numCircles = 8 } = $props();
</script>

<div
	class="absolute inset-0 flex items-center justify-center  [mask-image:linear-gradient(to_bottom,white,transparent)]"
>
	{#each { length: numCircles } as _, i}
		<div
			class="animate-ripple bg-foreground/30 absolute left-1/2 top-1/2 translate-x-1/2 translate-y-1/2 rounded-full border shadow-xl [--i:{i}]"
			style="width: {mainCircleSize + i * 70}px;
         height: {mainCircleSize + i * 70}px;
         opacity: {mainCircleOpacity - i * 0.03}; 
         animation-delay: {i * 0.08}s;
         border-style:{i === numCircles - 1 ? 'dashed' : 'solid'};
         border-width: 1px;
         border-color: rgba(var(--foreground-rgb), {(5 + i * 5) / 100});
        "
		></div>
	{/each}
</div>

<!-- 

 -->
