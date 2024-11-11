import { io, type Socket } from 'socket.io-client';

export let socket = $state<{value: Socket | null}>({value: null});
export let isConnected = $state<{value: boolean}>({value: false});
export let ragResponse = $state<{value: any}>({value: {}});

export function initializeSocket() {
    const socketInstance = io('http://localhost:5000', {
        transports: ['websocket'],
        autoConnect: true
    });

    socketInstance.on('connect', () => {
        console.log('Connected to WebSocket');
        isConnected.value = true;
    });

    socketInstance.on('disconnect', () => {
		console.log('Disconnected from WebSocket');
		isConnected.value = false;
	});

	socketInstance.on('rag_response', (data: any) => {
		ragResponse.value = data;
	});

	socket.value = socketInstance;

	return () => {
		socketInstance.disconnect();
		socket.value = null;
		isConnected.value = false;
	};
}