import request from '@/utils/request'
import Vue from 'vue'

export default {
    async getLastSync() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/getlastsync` )
        return data
    },
}