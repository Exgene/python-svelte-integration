<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import AnimatedButton from '$lib/components/ui/custom/AnimatedButton.svelte';
	import BorderBeam from '$lib/components/ui/custom/BorderBeam.svelte';
	import CardBody from '$lib/components/ui/custom/CardBody.svelte';
	import CardContainer from '$lib/components/ui/custom/CardContainer.svelte';
	import Elipses from '$lib/components/ui/custom/Elipses.svelte';
	import MultiDirection from '$lib/components/ui/custom/MultiDirection.svelte';
	import Pulse from '$lib/components/ui/custom/Pulse.svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import Input from '$lib/components/ui/input/input.svelte';
	import { isConnected, ragResponse } from '$lib/stores/socket.svelte';
	import { Stars } from 'lucide-svelte';
	import BackgroundBoxes from './BackgroundBoxes.svelte';
	import Lights from './Lights.svelte';

	let query = $state('');

	let computed = $state('');
	let loading = $state(false);
	let dialogOpen = $state(false);
	let showVisualization = $state(false);
	let node = $state({});
	let nodeNumber = $state(0);

	// let { data } = $props();

	async function handleSubmit(e: Event) {
		e.preventDefault();

		try {
			loading = true;
			await fetch('http://localhost:5000/api/rag', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ query })
			});
			const value = await fetch('/api/compile', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ data: ragResponse.value.result.generated_output })
			});
			const res = await value.json();
			computed = res.result;
			query = '';
		} catch (error) {
			console.error('Error:', error);
		} finally {
			loading = false;
		}
	}
	const result = $derived(computed);

	$effect(() => {
		console.log(result);
	});
</script>

<div class="w-[50rem] p-4 text-white">
	<div class="mt-3 p-6 text-start text-white/[0.7] sm:text-center">
		Connection Status:
		<span class={isConnected.value ? 'text-green-600' : 'text-red-600'}>
			{isConnected.value ? 'Connected' : 'Disconnected'}
		</span>
	</div>

	<form onsubmit={handleSubmit} class="mb-4 flex">
		<Input
			type="text"
			bind:value={query}
			placeholder="Enter your query..."
			class="mr-2 rounded border bg-gray-950 py-2"
		/>
		<Button
			type="submit"
			class="group flex h-full w-full items-center justify-center gap-1.5 rounded-lg border border-green-900 bg-gradient-to-br from-green-950 to-blue-950 text-gray-400 sm:w-36"
			disabled={!isConnected.value || loading}>Submit</Button
		>
	</form>
	{#if loading}
		<div class="flex items-center justify-center">
			<div
				class="relative flex h-[500px] w-full flex-col items-center justify-center overflow-hidden rounded-lg bg-transparent"
			>
				<p
					class="z-10 whitespace-pre-wrap text-center text-3xl font-medium tracking-tighter text-white"
				>
					Loading
				</p>
				<Pulse />
			</div>
		</div>
	{:else if ragResponse.value}
		<div class="mb-2 h-[400px] space-y-4 overflow-y-auto rounded bg-[#0b0b0f] p-4">
			<!-- {JSON.stringify(ragResponse.value.result)} -->
			{#if ragResponse.value.result}
				<CardContainer>
					<CardBody
						className="h-36 flex flex-col justify-center px-10 z-50"
						title={'Routed Node'}
						description={ragResponse.value.result.routed_node}
					/>
				</CardContainer>
				<!-- <CardContainer>
					<CardBody
						className="h-36 flex flex-col justify-center px-10 z-50"
						title={'Generated Response'}
						description={ragResponse.value.result.generated_output}
					/>
				</CardContainer> -->

				<!-- {JSON.stringify(ragResponse.value.result)} -->
				<div>
					<h3 class="mb-2 text-lg font-medium text-green-400">Generated Response:</h3>
					<div class="prose prose-invert overflow-y-auto whitespace-pre-wrap text-gray-200">
						{@html result}
					</div>
				</div>

				<Button
					class="flex items-center gap-2 rounded-full border border-slate-700 bg-black px-6 py-3 font-medium text-white transition-colors hover:border-slate-600 hover:bg-slate-800 active:scale-95"
					onclick={() => (showVisualization = !showVisualization)}
				>
					<Stars />
					Visualize
				</Button>

				{#if showVisualization}
					<MultiDirection
						class="mx-auto w-full"
						routedNode={ragResponse?.value?.result?.routed_node
							? parseInt(ragResponse.value.result.routed_node.match(/\d+/)?.[0] || '0')
							: 0}
					/>
				{/if}

				<Dialog.Root>
					<Dialog.Trigger
						class="flex w-full items-center gap-2 rounded-full border border-slate-700 bg-black px-6 py-3 font-medium text-white transition-colors hover:border-slate-600 hover:bg-slate-800 active:scale-95"
						onclick={() => !dialogOpen}
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="16"
							height="16"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							class="text-slate-400"
						>
							<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
							<path d="M14 2v6h6" />
							<path d="M16 13H8" />
							<path d="M16 17H8" />
							<path d="M10 9H8" />
						</svg>
						View Event Logs
					</Dialog.Trigger>
					<Dialog.Content class="h-[700px] w-[800px] overflow-y-auto bg-black text-white">
						<Dialog.Header>
							<Dialog.Title class="mb-4 text-xl font-bold">Event Logs</Dialog.Title>
							<Dialog.Description class="space-y-4">
								{#each ragResponse.value.result.events as event, index}
									<div class="rounded-lg border border-slate-700 p-4">
										<div class="mb-2 flex justify-between">
											<span class="text-green-400">Step {event.loop_step}</span>
											<span class="text-slate-400">Max Retries: {event.max_retries}</span>
										</div>

										<div class="mb-2">
											<span class="font-medium text-slate-300">Chat Message:</span>
											<p class="text-slate-400">{event.chat_message}</p>
										</div>

										{#if event.generation}
											<div>
												<span class="font-medium text-slate-300">Generation:</span>
												<p class="whitespace-pre-wrap text-slate-400">{event.generation}</p>
											</div>
										{/if}
									</div>
								{/each}
							</Dialog.Description>
						</Dialog.Header>
					</Dialog.Content>
				</Dialog.Root>
			{/if}
		</div>
	{/if}
</div>

<!-- <MultiDirection
	routedNode={ragResponse?.value?.result?.routed_node
		? parseInt(ragResponse.value.result.routed_node.match(/\d+/)?.[0] || '0')
		: 0}
/> -->

<style>
	/* Customize scrollbar for webkit browsers */
	::-webkit-scrollbar {
		width: 8px;
	}

	::-webkit-scrollbar-track {
		background: #1a1a1a;
		border-radius: 4px;
	}

	::-webkit-scrollbar-thumb {
		background: #333;
		border-radius: 4px;
	}

	::-webkit-scrollbar-thumb:hover {
		background: #444;
	}

	/* Firefox scrollbar styling */
	* {
		scrollbar-width: thin;
		scrollbar-color: #333 #1a1a1a;
	}
</style>
