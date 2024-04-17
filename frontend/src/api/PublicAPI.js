import request from '@/utils/request'
import Vue from 'vue'


export default {
    
    async checkBackendReady() {
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/ready` )
        return data
    },

    async checkDBConnected() {
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/connected` )
        return data
    },
    
    async checkDBPopulated() {
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/populated` )
        return data
    },    

}