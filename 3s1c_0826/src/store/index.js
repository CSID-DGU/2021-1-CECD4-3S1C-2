import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state:{
        dessert: []
    },
    mutations:{
        updating(state, content){
            state.dessert = content;
        }
    }
})