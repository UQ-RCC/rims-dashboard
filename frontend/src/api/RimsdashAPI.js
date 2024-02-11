import request from '@/utils/request'
import Vue from 'vue'


export default {
    
    async checkBackend() {
        console.log("checking backend")
        console.log("backend address:  " + Vue.prototype.$Config.backend)
        console.log("querying:  " + `${Vue.prototype.$Config.backend}/v1/ready`)
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/ready`)
        return data
    },

    async getUserByEmail(email) {
        let payload = {
            'email': email
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/userfromemail`, { params: payload } )
        return data
    },    

    async checkEmailIsAdmin(email) {
        let payload = {
            'email': email
        }        
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/checkadminbyemail`, { params: payload } )
        return data
    },

    async checkEmailIsInWhitelist(email) {
        let payload = {
            'email': email
        }        
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/checkwhitelistbyemail`, { params: payload } )
        return data
    },

    async getAllProjectsWithStates() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/allprojectswithstates` )
        return data
    },

    async getAllProjectsWithFullStates() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/allprojectswithfullstates` )
        return data
    },


    async getProjectDetails(project_id) {
        let payload = {
            'project_id': project_id
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/projectdetailwithusers`, { params: payload } )
        return data
    },
}