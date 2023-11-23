//import request from '@/utils/request'
import axios from 'axios'
import Vue from 'vue'

export default {

    async checkBackend() {
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/ready`)
        return data
    },

    async getUserByEmail(email) {
        let payload = {
            'email': email
        }
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/userfromemail`, { params: payload } )
        return data
    },    

    async checkEmailIsAdmin(email) {
        let payload = {
            'email': email
        }        
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/checkadminbyemail`, { params: payload } )
        return data
    },

    async getAllProjectsWithStates() {

        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/allprojectswithstates` )
        return data
    },

    async getAllProjectsWithFullStates() {

        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/allprojectswithfullstates` )
        return data
    },


    async getProjectDetails(project_id) {
        let payload = {
            'project_id': project_id
        }
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/projectdetailwithusers`, { params: payload } )
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

    async getUserProjectStates(user_login) {        
        let payload = {
            'login': user_login
        }
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/userprojectstates`, { params: payload } )
        return data
    },

    async getAllProjectsWithStates() {        

        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/allprojectstates` )
        return data
    },


    async getDefaultUserState() {        

        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/defaultuserstate` )
        return data
    },

    async getDefaultProjectStates() {        

        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/defaultuserprojectstates` )
        return data
    },

    async getDefaultProjectState() {        

        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/defaultprojectstate` )
        return data
    },    


    async checkEmailIsAdmin(email) {
        let payload = {
            'email': email
        }        
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/checkadminbyemail`, { params: payload } )
        return data
    },

    async getUserByEmail(email) {
        let payload = {
            'email': email
        }
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/userfromemail`, { params: payload } )
        return data
    },







    async getUserProjects(user_login) {
        let payload = {
            'login': user_login
        }        
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/userprojects`, { params: payload })
        return data
    },    

    async getProjectDetails(project_number) {
        let payload = {
            'project_number': project_number
        }        
        const { data } = await axios.get(`${Vue.prototype.$Config.backend}/rapi/v1/projectdetails`, { params: payload })
        return data
    },        

}
*/