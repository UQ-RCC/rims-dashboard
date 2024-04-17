import request from '@/utils/request'
import Vue from 'vue'

import { convertDatetime } from '../utils/helpers.js';


function convertSyncDates(data) {
    //convert the python datetime in the training request returns to a more readable date
    try {
        data.start_time = convertDatetime(data.start_time);
        data.end_time = convertDatetime(data.end_time);        
    }
    catch {
        Vue.$log.warn("datetime conversion failed for: " + data.id) 
    }
    
    return data

}

function convertSyncDatesByMap(data) {
    // Convert all the dates in a list of trequests

    const convertedData = data.map(item => {

        return convertSyncDates(item)

    });

    return convertedData;
}

export default {
    async getLastSync() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/getlastsync` )

        let converted_data = convertSyncDatesByMap(data)

        return converted_data
    },

    async getAllSyncEvents() {
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/allsyncs` )

        let converted_data = convertSyncDatesByMap(data)

        return converted_data
    },    

    async startManualSyncUpdate() {
        const response = await request.post(`${Vue.prototype.$Config.backend}/v1/manualsyncupdate` )

        Vue.$log.debug("manual sync return code: " + response.status) 

        return response
    },     

    async startManualSyncFull() {
        const response = await request.post(`${Vue.prototype.$Config.backend}/v1/manualsyncfull` )

        Vue.$log.debug("manual sync return code: " + response.status)         

        return response        
    },     

    async startManualSyncRebuild() {
        const response = await request.post(`${Vue.prototype.$Config.backend}/v1/manualsyncfullrebuild` )

        Vue.$log.debug("manual sync return code: " + response.status)         

        return response
    },         
}

