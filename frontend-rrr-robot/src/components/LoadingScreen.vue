<template>

  <div class="w-screen h-screen flex justify-center items-center">
    <div class="p-4 flex justify-center items-center flex-col">
      <POLogo/>
      <Loading/>
    </div>
  </div>
</template>

<script setup lang="ts">
import Loading from "@/components/Loading.vue";
import POLogo from "@/components/POLogo.vue";
</script>
