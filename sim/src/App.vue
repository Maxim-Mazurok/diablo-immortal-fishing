<script setup lang="ts">
import { ref } from "vue";
import { Application } from "vue3-pixi";
import RodBar from "./components/RodBar.vue";
import ProgressBar from "./components/ProgressBar.vue";

const progress = ref(0);

const handleProgress = (value: number) => {
  progress.value = value;
};
</script>

<template>
  <h1>Prototype WIP</h1>

  <h2>Simulates fishing progress: {{ (progress * 100).toFixed(0) }}%</h2>
  <Application :width="300" :height="30">
    <ProgressBar
      :width="300"
      :height="30"
      :color="0x00ff00"
      :duration="3"
      @progress="handleProgress"
    />
  </Application>

  <h2>Simulates Fish Movement when on the line, click/tap anywhere</h2>
  <Application :width="300" :height="30">
    <!-- Simulates Fish Movement when on the line, press space -->
    <RodBar :width="300" :height="30" :color="0xff0000" />
  </Application>
</template>
