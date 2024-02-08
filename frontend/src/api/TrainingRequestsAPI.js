import request from '@/utils/request'
import Vue from 'vue'
import VueLogger from 'vuejs-logger'

import { convertDatetime } from '../utils/helpers.js';

Vue.use(VueLogger)


function convertTrainingRequestDate(data) {
    //convert the python datetime in the training request returns to a more readable date
    try {
        data.date = convertDatetime(data.date);
    }
    catch {
        Vue.$log.warn("datetime conversion failed for: " + data.id) 
    }
    
    return data

}

function convertTrainingRequestDatesByMap(data) {
    // Convert all the dates in a list of trequests

    const convertedData = data.map(item => {

        return convertTrainingRequestDate(item)

    });

    return convertedData;
}

export default {
    async getAllTrainingRequests() {
        Vue.log.debug("getting all reqs: ")
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/alltrequests` )

        let converted_data = convertTrainingRequestDatesByMap(data)
        
        return converted_data
    },

    async getAllTrainingRequestsWithUsers() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/alltrequestswithusers` )
        
        let converted_data = convertTrainingRequestDatesByMap(data)
        
        return converted_data
    },

    async getTrainingRequestsById(trequest_id) {
        let payload = {
            'trequest_id': trequest_id
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/trequestsfilterbyid`, { params: payload } )
        
        let converted_data = convertTrainingRequestDatesByMap(data)
        
        return converted_data
    },

    async getTrainingRequestsByRequestType(substring) {
        let payload = {
            'search': substring
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/trequestsfilterbytype`, { params: payload } )
        
        let converted_data = convertTrainingRequestDatesByMap(data)
        
        return converted_data
    },

    async getTrainingRequestsByUser(substring) {
        let payload = {
            'substring': substring
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/trequestsfilterbyuser`, { params: payload } )
        
        let converted_data = convertTrainingRequestDatesByMap(data)
        
        return converted_data
    },


    async getTrainingRequestDetails(trequest_id) {
        let payload = {
            'trequest_id': trequest_id
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/v1/trequestdetail`, { params: payload } )

        let converted_data = convertTrainingRequestDate(data) 
        
        return converted_data
    },

}