<script setup>
import { defineProps } from "vue";

defineProps(["ordered", "payed"]);
</script>

<template>
  <div class="row text-center">
    <div class="col-sm-6">
      <div class="alert" :class="{ 'alert-danger': !ordered, 'alert-success': ordered }">
        {{ ordered ? "Bestellt" : "Noch nicht bestellt" }}
      </div>
    </div>
    <div class="col-sm-6">
      <div class="alert" :class="{ 'alert-danger': !payed, 'alert-success': payed }">
        {{ payed ? "Bezahlt" : "Nicht bezahlt" }}
      </div>
    </div>
  </div>
</template>
