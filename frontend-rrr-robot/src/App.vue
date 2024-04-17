<template>
  <Toaster />

  <LoadingScreen v-if="isLoading" />

  <div v-else class="min-h-screen bg-gray-100 flex flex-col items-center justify-start pt-8">
    <div class="w-full max-w-6xl px-4 md:px-8 lg:px-12">

      <h1>Robot Controller</h1>

      <Tabs default-value="manual" class="w-full">

        <TabsContent value="manual" class="h-96">

          <h2 class="font-bold text-4xl pt-4 pb-4">Manual</h2>

          <div class="flex flex-col gap-2">
            <div class="flex gap-1">
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
            </div>

            <div class="flex gap-1">
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
          </div>


        </TabsContent>
        <TabsContent value="code" class="h-96">

          <h2 class="font-bold text-4xl pt-4 pb-4">Program</h2>

          <div id="command" class="w-full flex justify-around items-center gap-1">
            <Select class="w-full" v-model="selectedCommand">
              <SelectTrigger>
                <SelectValue placeholder="Select command" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Commands</SelectLabel>
                  <SelectItem value="move_to">
                    move_to
                  </SelectItem>
                  <SelectItem value="sleep">
                    sleep
                  </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <Select class="w-full" v-if="selectedCommand === 'move_to'">
              <SelectTrigger>
                <SelectValue placeholder="Select position" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Positions</SelectLabel>
                  <SelectItem value="apple">
                    1
                  </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <Select class="w-full" v-if="selectedCommand === 'sleep'">
              <SelectTrigger>
                <SelectValue placeholder="Select time" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Positions</SelectLabel>
                  <SelectItem value="1">
                    1s
                  </SelectItem>
                  <SelectItem value="2">
                    2s
                  </SelectItem>
                  <SelectItem value="3">
                    3s
                  </SelectItem>
                  <SelectItem value="4">
                    4s
                  </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <Button>
              <Save />
            </Button>
            <Button variant="destructive">
              <Trash2 />
            </Button>
          </div>

          <Button class="mt-5 mb-5 rounded-full w-[80px] h-[80px]">
            <Plus />
          </Button>

          <Button class="mt-5 mb-5 rounded-full w-[80px] h-[80px] ml-5">
            <Play />
          </Button>

        </TabsContent>
        <TabsContent value="db" class="h-96">

          <h2 class="font-bold text-4xl pt-4 pb-4">Database</h2>

          <Table>
            <TableCaption>A list of saved positions</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>id</TableHead>
                <TableHead>theta1</TableHead>
                <TableHead>theta2</TableHead>
                <TableHead>theta3</TableHead>
                <TableHead>x</TableHead>
                <TableHead>y</TableHead>
                <TableHead>z</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="invoice in invoices" :key="invoice.invoice">
                <TableCell class="font-medium">
                  {{ invoice.invoice }}
                </TableCell>
                <TableCell>{{ invoice.paymentStatus }}</TableCell>
                <TableCell>{{ invoice.paymentMethod }}</TableCell>
                <TableCell class="text-right">
                  {{ invoice.totalAmount }}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>

        </TabsContent>
        <TabsList class="w-full flex justify-around items-center">
          <TabsTrigger value="manual" class="w-1/3">
            JOG
          </TabsTrigger>
          <TabsTrigger value="code" class="w-1/3">
            CODE
          </TabsTrigger>
          <TabsTrigger value="db" class="w-1/3">
            DB
          </TabsTrigger>
        </TabsList>
      </Tabs>

      <footer class="w-full sticky bottom-0 flex justify-around border flex-col mt-5">
        <div class="w-full flex justify-around">
          <div>
            <div>theta1</div>
            {{ theta1 }}
          </div>

          <div>
            <div>theta2</div>
            {{ theta2 }}
          </div>

          <div>
            <div>theta3</div>
            {{ theta3 }}
          </div>

          <div>
            <div>x</div>
            {{ x }}
          </div>

          <div>
            <div>y</div>
            {{ y }}
          </div>

          <div>
            <div>z</div>
            {{ z }}
          </div>
        </div>

        <Button class="w-full mt-3" @click.prevent="savePositionToDB">
          Save to database
        </Button>
      </footer>

    </div>
  </div>
</template>

<script setup lang="ts">
import {Save, Trash2, Plus, Play} from 'lucide-vue-next'
import {Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue} from '@/components/ui/select'
import {Button} from '@/components/ui/button';
import {onMounted, ref} from 'vue';
import io from 'socket.io-client';
import {Tabs, TabsTrigger, TabsList, TabsContent} from "@/components/ui/tabs";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useToast } from '@/components/ui/toast/use-toast'
import { Toaster } from "@/components/ui/toast"
import { Command, Position } from "@/types.ts";
import LoadingScreen from "@/components/LoadingScreen.vue";

const url = 'http://localhost:5000/save-position'

const socket = io('http://localhost:5000');
const serverResponse = ref('');
const isConnected = ref(false);

const isLoading = ref(false)

const selectedCommand = ref("")
const numberOfCommands = ref(0)
ref([]);
const theta1 = ref(Math.round(serverResponse.theta1 * 100) / 100)
const theta2 = ref(Math.round(serverResponse.theta2 * 100) / 100)
const theta3 = ref(Math.round(serverResponse.theta3 * 100) / 100)
const x = ref(Math.round(serverResponse.x * 100) / 100)
const y = ref(Math.round(serverResponse.y * 100) / 100)
const z = ref(Math.round(serverResponse.z * 100) / 100)

const { toast } = useToast()

const savePositionToDB = async (position: Position) => {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(position)
    })
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const responseData = await response.json()

    toast({
      title: 'Success!',
      description: 'Position saved successfully'
    })
  } catch (e) {
    toast({
      title: 'Oops',
      description: 'Something went wrong',
    })
  }
}

const saveCommandToDB = async (command: Command) => {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(command)
    })
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const responseData = await response.json()

    toast({
      title: 'Success!',
      description: 'Position saved successfully'
    })
  } catch (e) {
    toast({
      title: 'Oops',
      description: 'Something went wrong',
    })
  }
}

const fetchPositionsFromDB = async () => {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: { 'Content-Type': 'application/json' },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData: Position[] = await response.json()


  } catch (e) {
    toast({
      title: 'Oops',
      description: 'Something went wrong'
    })
  }
}

socket.on('connect', () => {
  isConnected.value = true;
});
socket.on('angles_data', (data) => {
  serverResponse.value = data;
});
const onTheta1Stop = () => {
  socket.emit('send-command', {name: 'stop_theta1', body: {}});
};
const onTheta3Stop = () => {
  socket.emit('send-command', {name: 'stop_theta3', body: {}});
};
const onTheta1Plus = () => {
  socket.emit('send-command', {name: 'theta1+', body: {}});
};
const onTheta1Minus = () => {
  socket.emit('send-command', {name: 'theta1-', body: {}});
};
const onTheta3Plus = () => {
  socket.emit('send-command', {name: 'theta3+', body: {}});
};
const onTheta3Minus = () => {
  socket.emit('send-command', {name: 'theta3-', body: {}});
};

</script>
