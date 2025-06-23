<template>
  <graphics @render="drawBar" />
</template>

<script setup lang="ts">
import { Graphics } from "pixi.js";
import { onBeforeUnmount, onMounted, ref } from "vue";
import { onTick } from "vue3-pixi";

const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 30 },
  color: { type: Number, default: 0xff0000 },
  speed: { type: Number, default: 100 }, // px/sec
  barRatio: { type: Number, default: 0.2 }, // 20% of width
  stopMin: { type: Number, default: 0.5 }, // min stop duration (sec)
  stopMax: { type: Number, default: 1.5 }, // max stop duration (sec)
  moveMin: { type: Number, default: 0.7 }, // min move duration (sec)
  moveMax: { type: Number, default: 2.0 }, // max move duration (sec)
});

const barWidth = props.width * props.barRatio;
const x = ref(Math.random() * (props.width - barWidth));
const direction = ref(Math.random() < 0.5 ? -1 : 1); // -1: left, 1: right
const stopped = ref(false);
let timer = 0;
let phaseDuration = 0;

function randomBetween(a: number, b: number) {
  return a + Math.random() * (b - a);
}

function startMovePhase() {
  stopped.value = false;
  direction.value = Math.random() < 0.5 ? -1 : 1;
  phaseDuration = randomBetween(props.moveMin, props.moveMax);
  timer = 0;
}

function startStopPhase() {
  stopped.value = true;
  phaseDuration = randomBetween(props.stopMin, props.stopMax);
  timer = 0;
}

function nextPhase() {
  if (stopped.value) {
    startMovePhase();
  } else {
    startStopPhase();
  }
}

onMounted(() => {
  startMovePhase();
});

onTick((delta) => {
  const dt = delta / 60;
  timer += dt;

  if (!stopped.value) {
    x.value += direction.value * props.speed * dt;

    // Clamp and reverse direction if hitting bounds
    if (x.value < 0) {
      x.value = 0;
      direction.value = 1;
    } else if (x.value > props.width - barWidth) {
      x.value = props.width - barWidth;
      direction.value = -1;
    }
  }

  if (timer >= phaseDuration) {
    nextPhase();
  }
});

function drawBar(g: Graphics) {
  g.clear();
  g.beginFill(props.color);
  g.drawRect(x.value, 0, barWidth, props.height);
  g.endFill();
}
</script>
