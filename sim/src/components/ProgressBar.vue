<template>
  <graphics @render="drawBar" />
</template>

<script setup lang="ts">
import { Graphics } from "pixi.js";
import { ref } from "vue";
import { onTick } from "vue3-pixi";

const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 30 },
  color: { type: Number, default: 0x00ff00 },
  duration: { type: Number, default: 2 }, // seconds
});

const emit = defineEmits(["complete", "progress"]);

const progress = ref(0);
const elapsed = ref(0);

onTick((delta) => {
  if (progress.value < 1) {
    elapsed.value += delta / 60;
    progress.value = Math.min(elapsed.value / props.duration, 1);
    emit("progress", progress.value);
  } else {
    emit("complete"); // TODO: optimize to only emit once
  }
});

const drawBar = (g: Graphics) => {
  g.clear();
  // NOTE: tried non-deprecated approach, but it didn't work
  g.beginFill(props.color);
  g.drawRect(0, 0, props.width * progress.value, props.height);
  g.endFill();
};
</script>
