<template>
  <v-simple-table dense>
    <template v-slot:default>      
      <thead>
        <tr>
          <th class="text-left">Name</th>
          <th class="text-left">Calories</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in desserts" :key="item.name">
          <td>{{ item.name }}</td>
          <td>{{ item.Calories }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
import axios from "axios";
export default {  
  data() {
    return {
      desserts: null      
    };
  },
  created() {
    axios.get("http://localhost:8080/api/data").then((res) => {
      // console.log(res);      
      this.desserts = res.data.map;
      console.log(this.desserts);      
    });    
  },
};
</script>