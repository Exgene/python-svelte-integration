<script lang="ts">
	import { cn } from '$lib/utils';
	import { onMount, tick } from 'svelte';
	import { cubicOut } from 'svelte/easing';

	let className: any = '';
	export { className as class };
	export let containerRef;
	export let fromRef;
	export let toRef;
	export let curvature = 0;
	export let reverse = false;
	export let duration = Math.random() * 3 + 4;
	export let delay = 0;
	export let pathColor = 'gray';
	export let pathWidth = 2;
	export let pathOpacity = 0.2;
	export let gradientStartColor = '#ffaa40';
	export let gradientStopColor = '#9c40ff';
	export let startXOffset = 0;
	export let startYOffset = 0;
	export let endXOffset = 0;
	export let endYOffset = 0;
	export let correctPath = 0;

	const id = crypto.randomUUID().slice(0, 8);

	let pathD = '';
	let svgDimensions = { width: 0, height: 0 };
	let gradientX1 = '0%';
	let gradientX2 = '10%';

	let animationFrame: number;

	function updatePath() {
		let containerRect = containerRef?.getBoundingClientRect();
		let rectA = fromRef?.getBoundingClientRect();
		let rectB = toRef?.getBoundingClientRect();

		if (!containerRect || !rectA || !rectB) return;

		svgDimensions = {
			width: containerRect.width,
			height: containerRect.height
		};

		let startX = rectA.left - containerRect.left + rectA.width / 2 + startXOffset;
		let startY = rectA.top - containerRect.top + rectA.height / 2 + startYOffset;
		let endX = rectB.left - containerRect.left + rectB.width / 2 + endXOffset;
		let endY = rectB.top - containerRect.top + rectB.height / 2 + endYOffset;

		let controlY = startY - curvature;
		pathD = `M ${startX},${startY} Q ${(startX + endX) / 2},${controlY} ${endX},${endY}`;
	}

	function animateGradient(timestamp: number) {
		const progress = (timestamp % (duration * 1000)) / (duration * 1000);

		if (reverse) {
			gradientX1 = `${100 - progress * 100}%`;
			gradientX2 = `${110 - progress * 100}%`;
		} else {
			gradientX1 = `${progress * 100}%`;
			gradientX2 = `${progress * 100 + 10}%`;
		}

		animationFrame = requestAnimationFrame(animateGradient);
	}

	onMount(async () => {
		await tick();
		updatePath();

		// Start animation after delay
		setTimeout(() => {
			animationFrame = requestAnimationFrame(animateGradient);
		}, delay * 1000);

		const resizeObserver = new ResizeObserver(() => {
			updatePath();
		});

		if (containerRef) {
			resizeObserver.observe(containerRef);
		}

		return () => {
			resizeObserver.disconnect();
			if (animationFrame) {
				cancelAnimationFrame(animationFrame);
			}
		};
	});
</script>

<svg
	fill="none"
	width={svgDimensions.width}
	height={svgDimensions.height}
	xmlns="http://www.w3.org/2000/svg"
	class={cn('pointer-events-none absolute left-0 top-0 transform-gpu stroke-2', className)}
	viewBox={`0 0 ${svgDimensions.width} ${svgDimensions.height}`}
>
	<path
		d={pathD}
		stroke={pathColor}
		stroke-width={pathWidth}
		stroke-opacity={correctPath === 0 ? pathOpacity : 0.6}
		stroke-linecap="round"
	/>
	<path
		d={pathD}
		stroke-width={pathWidth}
		stroke={`url(#${id})`}
		stroke-opacity="1"
		stroke-linecap="round"
	/>
	<defs>
		<linearGradient
			{id}
			gradientUnits="userSpaceOnUse"
			x1={gradientX1}
			x2={gradientX2}
			y1="0%"
			y2="0%"
			class="transform-gpu"
		>
			<stop offset="0%" stop-color={gradientStartColor} stop-opacity="0" />
			<stop offset="40%" stop-color={gradientStartColor} />
			<stop offset="80%" stop-color={gradientStopColor} />
			<stop offset="100%" stop-color={gradientStopColor} stop-opacity="0" />
		</linearGradient>
	</defs>
</svg>
