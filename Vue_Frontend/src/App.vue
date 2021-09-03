<template>
  <div>
    <BasicComponent></BasicComponent>
    <!-- <Chart></Chart> -->
    
  </div>
</template>

<script>
import BasicComponent from "./components/BasicComponent.vue";
import Chart from "./components/Chart.vue";
import Data from "./components/Data.vue";

export default {
  name: "App",
  components: {
    BasicComponent: BasicComponent,
    Chart: Chart,
    Data: Data,
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
