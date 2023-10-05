//import request from '@/utils/request'
import axios from 'axios'
import Vue from 'vue'

export default {
    async getUserList() {
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/userlist`)
        return data
    },

    async getUserState(user_login) {        
        let payload = {
            'login': user_login
        }
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/userstate`, { params: payload } )
        return data
    },

}