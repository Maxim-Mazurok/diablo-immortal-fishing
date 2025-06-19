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
  pushVelocity: { type: Number, default: 500 }, // rightward boost speed (px/sec)
  friction: { type: Number, default: 3500 }, // how quickly the boost slows down (px/sec^2)
  // TODO: probably get rid of friction and push velocity, looks like in the game it just jumps to the right instantly, consider checking screencast, doesn't matter too much tho
});

const x = ref(props.width);
const rightwardVelocity = ref(0); // push impulse

onTick((delta) => {
  const dt = delta / 60;

  // Move left at constant speed
  x.value -= props.speed * dt;

  // Apply rightward velocity if any
  if (rightwardVelocity.value > 0) {
    x.value += rightwardVelocity.value * dt;
    rightwardVelocity.value = Math.max(
      rightwardVelocity.value - props.friction * dt,
      0
    );
  }

  // Clamp to left bound
  if (x.value < 0) {
    x.value = 0;
    rightwardVelocity.value = 0;
  }
});

function drawLine(g: Graphics) {
  g.clear();
  g.lineStyle(2, props.color);
  g.moveTo(x.value, 0);
  g.lineTo(x.value, props.height);
}

function onKeydown(e: KeyboardEvent) {
  if (e.code === "Space") {
    rightwardVelocity.value += props.pushVelocity;
  }
}

onMounted(() => {
  window.addEventListener("keydown", onKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", onKeydown);
});
</script>
