import request from '@/utils/request'
import Vue from 'vue'

export default {
    async getUserList() {
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/api/v1/userlist`)
        return data
    },

    // get a collection
    //NOTE: param passing not verified
    async getState(user_login) {        
        let payload = {
            'login': user_login
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/api/v1/state/`, payload)
        return data
    },

    async getUserProjects(user_login) {
        let payload = {
            'login': user_login
        }        
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/api/v1/userprojects/`, payload)
        return data
    },    

    async getProjectDetails(project_number) {
        let payload = {
            'project_number': project_number
        }        
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/api/v1/projectdetails/`, payload)
        return data
    },        

}