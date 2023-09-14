//import request from '@/utils/request'
import axios from 'axios'
import Vue from 'vue'

export default {
    async getUserList() {
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/api/v1/userlist`)
        return data
    },

    async getUserState(user_login) {        
        let payload = {
            'login': user_login
        }
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/api/v1/userstate`, { params: payload } )
        return data
    },

    async getUserProjectStates(user_login) {        
        let payload = {
            'login': user_login
        }
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/api/v1/userprojectstates`, { params: payload } )
        return data
    },

    async getUserProjects(user_login) {
        let payload = {
            'login': user_login
        }        
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/api/v1/userprojects`, { params: payload })
        return data
    },    

    async getProjectDetails(project_number) {
        let payload = {
            'project_number': project_number
        }        
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/api/v1/projectdetails`, { params: payload })
        return data
    },        

}