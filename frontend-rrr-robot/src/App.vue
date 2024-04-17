<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center justify-start pt-8">
    <div class="w-full max-w-6xl px-4 md:px-8 lg:px-12">
      <h1>Manual</h1>

      <Button 
        @mousedown="onTheta1Plus"
        @mouseup="onTheta1Stop"
      >
        Theta1+
      </Button>
      <Button 
        @mousedown="onTheta1Minus" 
        @mouseup="onTheta1Stop"
      >
        Theta1-
      </Button>

      <Button
        @mousedown="onTheta3Plus"
        @mouseup="onTheta3Stop"
      >
        Theta3+
      </Button>
      <Button 
        @mousedown="onTheta3Minus" 
        @mouseup="onTheta3Stop"
      >
        Theta3-
      </Button>

    </div>
    <footer class="w-full h-96">
      <div>theta1: {{ serverResponse.theta1 }}</div>
      <div>theta2: {{ serverResponse.theta2 }}</div>
      <div>theta3: {{ serverResponse.theta3 }}</div>

      <div>x: {{ serverResponse.x }}</div>
      <div>y: {{ serverResponse.y }}</div>
      <div>z: {{ serverResponse.z }}</div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import {Button} from '@/components/ui/button';
import { onMounted, ref } from 'vue';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');
const serverResponse = ref('');
const isConnected = ref(false); 

socket.on('connect', () => {
  isConnected.value = true;
});

socket.on('angles_data', (data) => { serverResponse.value = data; });

const onTheta1Stop = () => { socket.emit('send-command', {name: 'stop_theta1', body: {}}); };
// 
const onTheta3Stop = () => { socket.emit('send-command', {name: 'stop_theta3', body: {}}); };

const onTheta1Plus = () => { socket.emit('send-command', {name: 'theta1+', body: {}}); };
const onTheta1Minus = () => { socket.emit('send-command', {name: 'theta1-', body: {}}); };

//

const onTheta3Plus = () => { socket.emit('send-command', {name: 'theta3+', body: {}}); };
const onTheta3Minus = () => { socket.emit('send-command', {name: 'theta3-', body: {}}); };

</script>
