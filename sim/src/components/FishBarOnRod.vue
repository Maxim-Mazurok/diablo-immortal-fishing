<template>
  <graphics @render="drawLine" />
</template>

<script setup lang="ts">
import { Graphics } from "pixi.js";
import { onBeforeUnmount, onMounted, ref, computed } from "vue";
import { onTick } from "vue3-pixi";

const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 30 },
  color: { type: Number, default: 0xff0000 },
  speed: { type: Number, default: 110 }, // constant leftward speed (px/sec)
  jumpDistance: { type: Number, default: 35 }, // how far to jump right on click
  barRatio: { type: Number, default: 0.2 }, // 20% of width
  stopMin: { type: Number, default: 0.5 },
  stopMax: { type: Number, default: 1.5 },
  moveMin: { type: Number, default: 0.7 },
  moveMax: { type: Number, default: 2.0 },
  barSpeed: { type: Number, default: 100 }, // px/sec for Rod bar
});

const x = ref(props.width); // vertical line position

// Rod bar logic
const barWidth = props.width * props.barRatio;
const barX = ref((props.width - barWidth) / 2);
const direction = ref(Math.random() < 0.5 ? -1 : 1);
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
  startStopPhase();
  window.addEventListener("click", onClick);
});

onBeforeUnmount(() => {
  window.removeEventListener("click", onClick);
});

onTick((delta) => {
  const dt = delta / 60;

  // Move vertical line left at constant speed
  x.value -= props.speed * dt;
  if (x.value < 0) x.value = 0;

  // Rod bar movement
  timer += dt;
  if (!stopped.value) {
    barX.value += direction.value * props.barSpeed * dt;
    if (barX.value < 0) {
      barX.value = 0;
      direction.value = 1;
    } else if (barX.value > props.width - barWidth) {
      barX.value = props.width - barWidth;
      direction.value = -1;
    }
  }
  if (timer >= phaseDuration) {
    nextPhase();
  }
});

// Collision detection: is the line within the bar?
const isColliding = computed(() => {
  return x.value >= barX.value && x.value <= barX.value + barWidth;
});

function drawLine(g: Graphics) {
  g.clear();
  // Draw Rod bar, green if colliding, red otherwise
  g.beginFill(isColliding.value ? 0x00ff00 : 0xff0000);
  g.drawRect(barX.value, 0, barWidth, props.height);
  g.endFill();
  // Draw vertical line
  g.lineStyle(2, props.color);
  g.moveTo(x.value, 0);
  g.lineTo(x.value, props.height);
}

function onClick() {
  x.value = Math.min(x.value + props.jumpDistance, props.width);
}
</script>
