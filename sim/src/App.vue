<script setup lang="ts">
import { ref } from "vue";
import { Application } from "vue3-pixi";
import FishBar from "./components/FishBar.vue";
import FishBarOnRod from "./components/FishBarOnRod.vue";
import ProgressBar from "./components/ProgressBar.vue";
import RodBar from "./components/RodBar.vue";

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

  <h2>Simulates Rod Movement when fish is on the line, click/tap anywhere</h2>
  <Application :width="300" :height="30">
    <!-- Simulates Fish Movement when on the line, press space -->
    <RodBar :width="300" :height="30" :color="0xff0000" />
  </Application>

  <h2>Simulates Fish Bar</h2>
  <Application :width="300" :height="30">
    <FishBar :width="300" :height="30" :color="0x0000ff" />
  </Application>

  <h2>Simulates Rod on Fish Bar</h2>
  <Application :width="300" :height="30">
    <FishBarOnRod />
  </Application>
</template>
