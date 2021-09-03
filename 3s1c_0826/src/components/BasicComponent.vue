<template>
  <div id="app">
    <div id="masthead">
      <h1>3S1C</h1>
    </div>
    <hr />
    <div id="menu">
      <Button>누적 데이터</Button>
      <Button>섹션 통계</Button>
      <Button>시간 통계</Button>
      <Button>연령 통계</Button>
    </div>
    <hr />
    <div id="container">
      <div id="first">
        <!-- <Chart></Chart> -->
        <v-simple-table dense>
                
            <thead>
              <tr>
                <th class="text-left">Name</th>
                <th class="text-left">Calories</th>
              </tr>
            </thead>
            <tbody>
                <tr v-for="item in this.$store.state.dessert" :key="item.name">
                  <td>{{ item.name }}</td>
                  <td>{{ item.Calories }}</td>
                </tr>
            </tbody>
          
        </v-simple-table>
        <div id="firstContent">
          <Paper variant="outlined"><Button>기획분석</Button></Paper>
        </div>
        <div id="firstContent">
          <Paper variant="outlined"><Button>Questions</Button></Paper>
        </div>
      </div>
      <div id="second">
        <div id="title">
          <h1>분석판</h1>
        </div>
        <v-Divider variant="middle" />
        <div id="content">
          <!-- <Data></Data>           -->                  
          <li v-for ="item in this.$store.state.dessert" :key="item.name">
            {{item.name}}
            {{item.Calories}}
          </li>
        </div>
      </div>
      <div id="third"></div>
    </div>
  </div>
</template>

<script>
import Data from "./Data.vue"
import Chart from "./Chart.vue"
import axios from "axios"

export default {
  el: "#app",
  components: {
    'Data' : Data,
    'Chart' : Chart,
  },
  data() {
    return {
      // ok: this.$store.state.dessert
    };
  },
  methods:{
    update(){
      axios.get("http://localhost:8080/api/data").then((res) => {
      console.log(res)
      const vd = res

      this.$store.commit('updating', vd.data)
      console.log(this.$store.state.dessert)
      });
    }
  },  
  created(){
    this.update();
    // console.log(this.ok)
  }
  
};
</script>


<style scoped>
#container {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  /* border: solid; */
  width: 100%;
  height: 100vh;
}
#first {
  display: flex;
  grid-column-start: 0;
  grid-column-end: 2;
  flex-direction: column;
  border-right: 1px solid grey;
  /* magin: '3px'; */
  /* border: solid; */
}
#second {
  /* display: 'grid'; */
  grid-column-start: 2;
  grid-column-end: 10;
  grid-template-rows: repeat(6, 1fr);
  /* border: solid; */
  border-right: 1px solid grey;
}
#title {
  display: flex;
  grid-row-start: 0;
  grid-row-end: 1;
  /* border: solid; */
  justify-content: center;
  align-items: center;
}
#content {
  display: flex;
  grid-row-start: 1;
  grid-row-end: 5;
  /* border: solid; */
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
#third {
  display: flex;
  grid-column-start: 11;
  grid-column-end: 12;
  /* borderLeft: '1px solid gray';             */
  /* border: solid; */
}
#thirdContent {
  display: flex;
  justify-content: center;
  align-items: center;
}
#menu {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  margin-bottom: 5px;
  margin-top: 1px;
}
#masthead {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0px;
}
#firstContent {
  margin-top: 10px;
}
#chartSize {
  width: 100%;
  height: 50%;
}
</style>