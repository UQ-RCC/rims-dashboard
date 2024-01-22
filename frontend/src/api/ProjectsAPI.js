import request from '@/utils/request'
import Vue from 'vue'

export default {
    async getAllProjectsWithStates() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/allprojectswithstates` )
        return data
    },

    async getAllProjectsWithFullStates() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/allprojectswithfullstates` )
        return data
    },

    async getProjectDetails(project_id) {
        let payload = {
            'project_id': project_id
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/projectdetailwithusers`, { params: payload } )
        return data
    },

    async getProjectById(project_id) {
        let payload = {
            'project_id': project_id
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/projectgetbyid`, { params: payload } )
        return data
    },

    async getProjectsByTitle(substring) {
        let payload = {
            'search': substring
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/projectsgetbytitle`, { params: payload } )
        return data
    },

    async getProjectsByGroup(substring) {
        let payload = {
            'search': substring
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/projectsgetbygroup`, { params: payload } )
        return data
    },

    async getProjectsByUser(substring) {
        let payload = {
            'search': substring
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/projectsgetbyuser`, { params: payload } )
        return data
    },
}
/*
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
*/