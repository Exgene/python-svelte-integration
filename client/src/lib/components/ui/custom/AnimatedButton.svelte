<script lang="ts">
	import { fade, fly } from 'svelte/transition';

	export let buttonColor: string = '#000';
	export let buttonTextColor: string = '#fff';
	export let subscribeStatus: boolean = false;

	let isSubscribed = subscribeStatus;
</script>

{#if isSubscribed}
	<button
		transition:fade={{ duration: 200 }}
		on:click={() => (isSubscribed = !isSubscribed)}
		class="relative flex w-[200px] items-center justify-center overflow-hidden rounded-md bg-white p-[10px]"
	>
		<span
			in:fly={{ y: -50, duration: 200 }}
			class="relative block h-full w-full font-semibold text-white dark:text-black"
		>
			<slot name="changeText">Subscribed</slot>
		</span>
	</button>
{:else}
	<button
		transition:fade={{ duration: 200 }}
		style="background-color: {buttonColor}; color: {buttonTextColor};"
		on:click={() => (isSubscribed = !isSubscribed)}
		class="relative flex w-[200px] cursor-pointer items-center justify-center rounded-md border-none p-[10px]"
	>
		<span in:fly={{ x: -50, duration: 200 }} class="text-primary relative block font-semibold">
			<slot name="initialText">Subscribe</slot>
		</span>
	</button>
{/if}
