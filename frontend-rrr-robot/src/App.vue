<template>
  <Toaster/>

  <LoadingScreen v-if="isLoading"/>

  <div v-else class="min-h-screen bg-gray-100 flex flex-col items-center justify-start pt-8">
    <div class="w-full max-w-6xl px-4 md:px-8 lg:px-12">
      <Drawer>

        <h1>Robot Controller</h1>

        <Tabs default-value="manual" class="w-full">

          <TabsContent value="manual" class="overflow-auto h-[70vh]">

            <h2 class="font-bold text-4xl pt-4 pb-4">Manual</h2>

            <div class="flex flex-col gap-2 select-none">
              <div class="flex gap-1">
                <Button

                    @mousedown.prevent="onTheta1Plus"
                    @mouseup.prevent="onTheta1Stop"
                    @touchstart.prevent="onTheta1Plus"
                    @touchend.prevent="onTheta1Stop"
                >
                  Theta1+
                </Button>
                <Button

                    @mousedown.prevent="onTheta1Minus"
                    @mouseup.prevent="onTheta1Stop"
                    @touchstart.prevent="onTheta1Minus"
                    @touchend.prevent="onTheta1Stop"

                >
                  Theta1-
                </Button>
              </div>

              <div class="flex gap-1">
                <Button

                    @mousedown.prevent="onTheta2Plus"
                    @mouseup.prevent="onTheta2Stop"
                    @touchstart.prevent="onTheta2Plus"
                    @touchend.prevent="onTheta2Stop"
                >
                  Theta2+
                </Button>
                <Button

                    @mousedown.prevent="onTheta2Minus"
                    @mouseup.prevent="onTheta2Stop"
                    @touchstart.prevent="onTheta2Minus"
                    @touchend.prevent="onTheta2Stop"
                >
                  Theta2-
                </Button>
              </div>

              <div class="flex gap-1">
                <Button

                    @mousedown.prevent="onTheta3Plus"
                    @mouseup.prevent="onTheta3Stop"
                    @touchstart.prevent="onTheta3Plus"
                    @touchend.prevent="onTheta3Stop"
                >
                  Theta3+
                </Button>
                <Button

                    @mousedown.prevent="onTheta3Minus"
                    @mouseup.prevent="onTheta3Stop"
                    @touchstart.prevent="onTheta3Minus"
                    @touchend.prevent="onTheta3Stop"
                >
                  Theta3-
                </Button>
              </div>
            </div>

            <br>

            <div class="gap-2.5 flex items-center">
              <Button @click.prevent="percentOfPower = Math.min(percentOfPower + 10, 100)">+</Button>
              <span>{{ percentOfPower }}</span>
              <Button @click.prevent="percentOfPower = Math.max(percentOfPower - 10, 20)">-</Button>
            </div>

            <br>
            <br>
            <br>
            
            <Button @click.prevent="shutdown">Turn off system</Button>  

          </TabsContent>

          <TabsContent value="code" class="overflow-auto h-[70vh]">

            <h2 class="font-bold text-4xl pt-4 pb-4">Program</h2>
            <p>Always end program with move_to!</p>

            <Form v-slot="{setValues}" @submit="(values) => saveCodeToDB(values)">
              <div
                  v-for="(command, index) in code"
                  :key="command.id"
                  class="w-full flex justify-around items-center gap-3 m-1.5"
              >

                <FormField class="w-10/12" v-slot="{componentField}" :name="`name-${command.id}`">
                  <FormItem class="w-full">
                    <Select class="w-full" v-model="command.name" v-bind="componentField" :default-value="command.name">
                      <SelectTrigger>
                        <SelectValue placeholder="Select command"/>
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

                  </FormItem>
                </FormField>

                <FormField class="w-10/12" v-if="command.name === 'move_to'" v-slot="{componentField}"
                           :name="`body-${command.id}`">
                  <FormItem class="w-full">

                    <Select class="w-full" v-bind="componentField" :default-value="command.body">
                      <SelectTrigger>
                        <SelectValue placeholder="Select position"/>
                      </SelectTrigger>
                      <SelectContent>
                        <SelectGroup>
                          <SelectLabel>Positions</SelectLabel>
                          <SelectItem v-for="position in positions" :value="String(position.id)">
                            {{ position.id }}
                          </SelectItem>
                        </SelectGroup>
                      </SelectContent>
                    </Select>

                  </FormItem>
                </FormField>


                <FormField class="w-10/12" v-if="command.name === 'sleep'" v-slot="{componentField}"
                           :name="`body-${command.id}`">
                  <FormItem class="w-full">
                    <Select class="w-full" v-bind="componentField" :default-value="command.body">
                      <SelectTrigger>
                        <SelectValue placeholder="Select time"/>
                      </SelectTrigger>
                      <SelectContent>
                        <SelectGroup>
                          <SelectLabel>Time</SelectLabel>
                          <SelectItem value="0.3">0.3s</SelectItem>  
                          <SelectItem value="1">1s</SelectItem>
                          <SelectItem value="2">2s</SelectItem>
                          <SelectItem value="3">3s</SelectItem>
                          <SelectItem value="4">4s</SelectItem>
                        </SelectGroup>
                      </SelectContent>
                    </Select>
                  </FormItem>
                </FormField>

                <Button variant="destructive" @click.prevent="removeCommand(command.id)">
                  <Trash2/>
                </Button>
              </div>

              <Button type="submit" class="rounded-full w-[80px] h-[80px] mt-5" variant="outline">
                <Save/>
              </Button>

              <Button class="mt-5 mb-5 rounded-full w-[80px] h-[80px] ml-5" @click.prevent="addCommand"
                      variant="outline">
                <Plus/>
              </Button>

            </Form>

            <!--            <DrawerTrigger as-child>-->
            <Button
                class="mt-5 mb-5 rounded-full w-[80px] h-[80px]"
                @click.prevent="runProgram"
                :disabled="isRunProgramLoading"
            >
              <Loader2 class="animate-spin" v-if="isRunProgramLoading"/>
              <Play v-if="!isRunProgramLoading"/>
            </Button>

            <Button
                class="mt-5 mb-5 rounded-full w-[80px] h-[80px] ml-5"
                @click.prevent="generatePlots"
                :disabled="isGeneratePlotsLoading"
            >
              <Loader2 class="animate-spin" v-if="isGeneratePlotsLoading"/>
              <AreaChart v-if="!isGeneratePlotsLoading"/>
            </Button>
            <!--            </DrawerTrigger>-->

          </TabsContent>

          <TabsContent value="db" class="overflow-auto h-[70vh]">

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
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow v-for="position in positions" :key="position.id">
                  <TableCell>{{ position.id }}</TableCell>
                  <TableCell>{{ position.theta1 }}</TableCell>
                  <TableCell>{{ position.theta2 }}</TableCell>
                  <TableCell>{{ position.theta3 }}</TableCell>
                  <TableCell>{{ position.x }}</TableCell>
                  <TableCell>{{ position.y }}</TableCell>
                  <TableCell>{{ position.z }}</TableCell>
                  <TableCell>
                    <button @click.prevent="deletePositionFromDB(position.id)">remove</button>
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

        <footer
            class="ml-auto mr-auto  bottom-3 w-auto z-10 flex justify-around border flex-col mt-5 p-2 bg-white shadow-lg">
          <div class="w-full flex justify-around">
            <div class="w-1/6">
              <div class="w-full text-center">theta1</div>
              <div class="w-full h-full text-center" v-if="isConnected">{{ theta1 }}</div>
              <Skeleton v-else class="w-full h-[24px]"/>
            </div>
            <div class="w-1/6">
              <div class="w-full text-center">theta2</div>
              <div class="w-full h-full text-center" v-if="isConnected">{{ theta2 }}</div>
              <Skeleton v-else class="w-full h-[24px]"/>
            </div>
            <div class="w-1/6">
              <div class="w-full text-center">theta3</div>
              <div class="w-full h-full text-center" v-if="isConnected">{{ theta3 }}</div>
              <Skeleton v-else class="w-full h-[24px]"/>
            </div>
            <div class="w-1/6">
              <div class="w-full text-center">x</div>
              <div class="w-full h-full text-center" v-if="isConnected">{{ x }}</div>
              <Skeleton v-else class="w-full h-[24px]"/>
            </div>
            <div class="w-1/6">
              <div class="w-full text-center">y</div>
              <div class="w-full h-full text-center" v-if="isConnected">{{ y }}</div>
              <Skeleton v-else class="w-full h-[24px]"/>
            </div>
            <div class="w-1/6">
              <div class="w-full text-center">z</div>
              <div class="w-full h-full text-center" v-if="isConnected">{{ z }}</div>
              <Skeleton v-else class="w-full h-[24px]"/>
            </div>
          </div>

          <Button class="w-full mt-3" @click.prevent="savePositionToDB({x,y,z,theta1,theta2,theta3})">
            Save to database
          </Button>
        </footer>


        <DrawerContent>
          <div class="mx-auto w-full max-w-sm">
            <DrawerHeader>
              <DrawerTitle>Program Compilation</DrawerTitle>
              <DrawerDescription>You will be able to start program shortly</DrawerDescription>
            </DrawerHeader>

            <div class="w-full flex flex-col gap-3 items-start overflow-auto">


              <div class="w-full flex flex-col gap-3 items-start">

                <p>movement 1</p>

                <div class="flex justify-center items-center font-bold">
                  <DoneSmall/>
                  <p>Calculating points, cnt = 0.5</p>
                </div>

                <div class="flex justify-center items-center font-bold">
                  <LoadingSmall/>
                  <p>Calculating trajectory, step = 0.01s</p>
                </div>

                <div class="flex justify-center items-center font-bold">
                  <LoadingSmall/>
                  <p>Calculating velocities</p>
                </div>

                <div class="flex justify-center items-center font-bold">
                  <LoadingSmall/>
                  <p>Generating graphs</p>
                </div>

              </div>

              <div class="w-full flex flex-col gap-3 items-start">

                <p>movement 2</p>

                <div class="flex justify-center items-center font-bold">
                  <DoneSmall/>
                  <p>Calculating points, cnt = 0.5</p>
                </div>

                <div class="flex justify-center items-center font-bold">
                  <LoadingSmall/>
                  <p>Calculating trajectory, step = 0.01s</p>
                </div>

                <div class="flex justify-center items-center font-bold">
                  <LoadingSmall/>
                  <p>Calculating velocities</p>
                </div>

                <div class="flex justify-center items-center font-bold">
                  <LoadingSmall/>
                  <p>Generating graphs</p>
                </div>

              </div>

            </div>

            <!--            <DrawerFooter>-->
            <!--              <Button>Submit</Button>-->
            <!--              <DrawerClose as-child>-->
            <!--                <Button variant="outline">-->
            <!--                  Cancel-->
            <!--                </Button>-->
            <!--              </DrawerClose>-->
            <!--            </DrawerFooter>-->
          </div>
        </DrawerContent>

      </Drawer>

    </div>
  </div>
</template>

<script setup lang="ts">
import {Form, FormField, FormItem} from '@/components/ui/form'
import {Skeleton} from '@/components/ui/skeleton'
import {Play, Plus, Save, Trash2, AreaChart, Loader2} from 'lucide-vue-next'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select'
import {Button} from '@/components/ui/button';
import {onMounted, ref} from 'vue';
import io from 'socket.io-client';
import {Tabs, TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs";
import {Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow} from '@/components/ui/table'
import {useToast} from '@/components/ui/toast/use-toast'
import {Toaster} from "@/components/ui/toast"
import {Command, Position} from "@/types.ts";
import LoadingScreen from "@/components/LoadingScreen.vue";
import {parseCommandsToCode} from "@/utils.ts";
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from '@/components/ui/drawer'
import LoadingSmall from "@/components/LoadingSmall.vue";
import DoneSmall from "@/components/DoneSmall.vue";


const socket = io('http://192.168.1.28:5000');
let serverResponse = ref<never | {
  x: number,
  y: number,
  z: number,
  theta1: number,
  theta2: number,
  theta3: number
}>(undefined)
const isConnected = ref<boolean>(false);

const theta1 = ref<undefined | number>(undefined);
const theta2 = ref<undefined | number>(undefined);
const theta3 = ref<undefined | number>(undefined);
const x = ref<undefined | number>(undefined);
const y = ref<undefined | number>(undefined);
const z = ref<undefined | number>(undefined);

const percentOfPower = ref<number>(100)

// socket.on('connect', () => {
//
// });
socket.on('angles_data', (data) => {
  isConnected.value = true;
  serverResponse.value = data;
  updateValues()
});
const onTheta1Stop = () => {
  socket.emit('send-command', {name: 'stop_theta1', body: {}});
};
const onTheta2Stop = () => {
  socket.emit('send-command', {name: 'stop_theta2', body: {}});
};
const onTheta3Stop = () => {
  socket.emit('send-command', {name: 'stop_theta3', body: {}});
};
const onTheta1Plus = () => {
  socket.emit('send-command', {name: 'theta1+', body: {power: percentOfPower.value}});
};
const onTheta1Minus = () => {
  socket.emit('send-command', {name: 'theta1-', body: {power: percentOfPower.value}});
};
const onTheta2Plus = () => {
  socket.emit('send-command', {name: 'theta2+', body: {power: percentOfPower.value}});
};
const onTheta2Minus = () => {
  socket.emit('send-command', {name: 'theta2-', body: {power: percentOfPower.value}});
};
const onTheta3Plus = () => {
  socket.emit('send-command', {name: 'theta3+', body: {power: percentOfPower.value}});
};
const onTheta3Minus = () => {
  socket.emit('send-command', {name: 'theta3-', body: {power: percentOfPower.value}});
};

const updateValues = () => {
  theta1.value = Math.round(Number(serverResponse.value.theta1) * 100) / 100;
  theta2.value = Math.round(Number(serverResponse.value.theta2) * 100) / 100;
  theta3.value = Math.round(Number(serverResponse.value.theta3) * 100) / 100;
  x.value = Math.round(Number(serverResponse.value.x) * 100) / 100;
  y.value = Math.round(Number(serverResponse.value.y) * 100) / 100;
  z.value = Math.round(Number(serverResponse.value.z) * 100) / 100;
};

const {toast} = useToast()

const isLoading = ref(false)

const positions = ref<null | Position[]>(null)
const loading = ref<boolean>(false)

const isLoadingRunProgram = ref(false)

const code = ref<Command[]>([])


onMounted(() => {
  fetchPositionsFromDB()
  fetchCodeFromDB()
})

const addCommand = () => {
  code.value.push({id: code.value.length, name: '', body: ''})
}

const saveCodeToDB = async (values: { [key: string]: string }) => {
  const code = parseCommandsToCode(values)
  const url = 'http://192.168.1.28:5000/api/commands/1'
  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({code: code})
    })

    console.log(JSON.stringify({code: code}))

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    toast({
      title: 'Success',
      description: 'Program saved! Click RUN'
    })

  } catch (e) {
    toast({
      title: 'Oops',
      description: 'Failed to post code to db'
    })
  } finally {
    // loading.value = false
  }
}

const deletePositionFromDB = async (id: number) => {
  const url = `http://192.168.1.28:5000/api/positions/${id}`
  try {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {'Content-Type': 'application/json'},
      body: id
    })
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    await fetchPositionsFromDB()
    toast({
      title: 'Success!',
      description: 'Position deleted successfully'
    })
  } catch (e) {
    toast({
      title: 'Oops',
      description: 'Failed fetching code from db'
    })
  } finally {
    // loading.value = false
  }
}

const removeCommand = (id: number) => {
  code.value = code.value.filter(cmd => cmd.id !== id);
};

const isProgramRunning = ref(false)
const isRunProgramLoading = ref(false)
const runProgram = async () => {
  isRunProgramLoading.value = true
  const url = 'http://192.168.1.28:5000/api/run'
  try {
    const response = await fetch(url, {
      method: "POST",
    })
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    isProgramRunning.value = true
    return await response.json()
  } catch (e) {

  } finally {
    isRunProgramLoading.value = false
  }
}

const isRunEmergencyStopLoading = ref(false)
const runEmergencyStop = async () => {
  isRunEmergencyStopLoading.value = true
  const url = 'http://192.168.1.28:5000/api/stop'
  try {
    const response = await fetch(url, {
      method: "POST",
    })
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json()
  } catch (e) {

  } finally {
    isRunEmergencyStopLoading.value = false
  }
}

const isGeneratePlotsLoading = ref(false)
const generatePlots = async () => {
  const url = 'http://192.168.1.28:5000/api/plot'
  try {
    isGeneratePlotsLoading.value = true
    const response = await fetch(url, {
      method: "POST",
    })
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json()
  } catch (e) {

  } finally {
    isGeneratePlotsLoading.value = false
  }
}

const shutdown = async () => {
  const url = 'http://192.168.1.28:5000/api/turnoff'
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
    })

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json()
    code.value = JSON.parse(responseData.code)
    console.log(code.value)

  } catch (e) {
    toast({
      title: 'Oops',
      description: 'Failed fetching code from db'
    })
  } finally {
    // loading.value = false
  }
}

const fetchCodeFromDB = async () => {
  // loading.value = true
  const url = 'http://192.168.1.28:5000/api/commands/1'
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {'Content-Type': 'application/json'},
    })

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json()
    code.value = JSON.parse(responseData.code)
    console.log(code.value)

  } catch (e) {
    toast({
      title: 'Oops',
      description: 'Failed fetching code from db'
    })
  } finally {
    // loading.value = false
  }
}

const fetchPositionsFromDB = async () => {
  loading.value = true
  const url = 'http://192.168.1.28:5000/api/positions'
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {'Content-Type': 'application/json'},
    })

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData: Position[] = await response.json()
    positions.value = responseData
    console.log(positions.value)

  } catch (e) {
    toast({
      title: 'Oops',
      description: 'Failed fetching positions from db'
    })
  } finally {
    loading.value = false
  }
}

const savePositionToDB = async (position: Position) => {
  const url = 'http://192.168.1.28:5000/api/positions'
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(position)
    })
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    await fetchPositionsFromDB()
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
  const url = 'http://192.168.1.28:5000/api/commands'
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
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


</script>
