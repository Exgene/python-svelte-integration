<script lang="ts">
	import BorderBeam from '$lib/components/ui/custom/BorderBeam.svelte';
	import Particles from '$lib/components/ui/custom/Particles.svelte';
	import { initializeSocket } from '$lib/stores/socket.svelte';
	import '../app.css';
	import Lights from './Lights.svelte';
	let { children } = $props();

	$effect(() => {
		initializeSocket();
	});
</script>



<Particles className="absolute inset-0" refresh={true} />
<main class="dark block h-screen w-full overflow-hidden rounded-xl bg-black">
	<div class="bg-grid-white/[0.03] relative h-full w-full px-4">
		<BorderBeam />
		<div
			class="animate-moveUp relative z-[1] flex h-full w-full flex-col items-start justify-center sm:items-center"
		>
			<!-- <BackgroundBoxes r={10} c={10} /> -->
			<div class="relative w-full">
				<div
					class="absolute -top-12 left-0 aspect-square overflow-hidden rounded-lg border border-green-900 bg-gradient-to-br from-green-950/40 to-blue-950/40 p-1 backdrop-blur-md sm:left-1/2 sm:-translate-x-1/2"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="28"
						height="28"
						viewBox="0 0 24 24"
						fill="#ffffff"
						stroke="currentColor"
						stroke-width="1.2"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="lucide lucide-cloud"
						><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z" /></svg
					>
				</div>
			</div>
			<div
				class="bg-gradient-to-br from-white/60 via-neutral-300 to-black/[0.6] bg-clip-text text-start text-4xl font-bold text-transparent sm:text-center sm:text-5xl"
			>
				Input your query, Get Routed
			</div>
			<div class="mt-3 text-start text-white/[0.7] sm:text-center">
				Trusted by Trusted Companies and Trusted People
			</div>
			{@render children()}
		</div>
		<div class="animate-appear absolute bottom-0 left-0 z-0 h-full w-full">
			<div class="h-full w-full overflow-hidden">
				<div
					style="background: conic-gradient(from 0deg at 50% 50%, #3b82f6 0deg, #22d3ee 180deg, #facc15 360deg);"
					class="absolute inset-0 bottom-[500px] h-full w-full opacity-[0] blur-[75px]"
				></div>
			</div>
		</div>
	</div>
</main>
