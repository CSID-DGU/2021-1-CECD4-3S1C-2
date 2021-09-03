<template>
  <div>
    {{ ok }}
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      ok: "",
    };
  },
  read() {
    axios.get("http://localhost:8080/api/data").then((res) => {
      console.log(res);

      this.ok = res.data[0].name;
      console.log(this.ok);
    });
  },
  created(){
    this.read()
  }
};
</script>

<style scoped></style>
