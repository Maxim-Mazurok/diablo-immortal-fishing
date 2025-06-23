<template>
  <graphics @render="drawLine" />
</template>

<script setup lang="ts">
import { Graphics } from "pixi.js";
import { onBeforeUnmount, onMounted, ref } from "vue";
import { onTick } from "vue3-pixi";

const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 30 },
  color: { type: Number, default: 0xff0000 },
  speed: { type: Number, default: 100 }, // constant leftward speed (px/sec)
  jumpDistance: { type: Number, default: 50 }, // how far to jump right on click
});

const x = ref(props.width);

onTick((delta) => {
  const dt = delta / 60;

  // Move left at constant speed
  x.value -= props.speed * dt;

  // Clamp to left bound
  if (x.value < 0) {
    x.value = 0;
  }
});

function drawLine(g: Graphics) {
  g.clear();
  g.lineStyle(2, props.color);
  g.moveTo(x.value, 0);
  g.lineTo(x.value, props.height);
}

function onClick() {
  x.value = Math.min(x.value + props.jumpDistance, props.width);
}

onMounted(() => {
  window.addEventListener("click", onClick);
});

onBeforeUnmount(() => {
  window.removeEventListener("click", onClick);
});
</script>
