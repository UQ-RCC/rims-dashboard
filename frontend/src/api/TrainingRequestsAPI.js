import request from '@/utils/request'
import Vue from 'vue'
import { convertDatetime } from '../utils/helpers.js';


function convertTrainingRequestDates(data) {

    // Convert each datetime string to a more human-readable format
    const convertedData = data.map(item => {
       item.date = convertDatetime(item.date);

       return item
    });

    return convertedData;
}


export default {
    async getAllTrainingRequests() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/alltrequests` )

        let converted_data = convertTrainingRequestDates(data)
        
        return converted_data
    },

    async getAllTrainingRequestsWithUsers() {

        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/alltrequestswithusers` )
        
        let converted_data = convertTrainingRequestDates(data)
        
        return converted_data
    },

    async getTrainingRequestDetails(trequest_id) {
        let payload = {
            'trequest_id': trequest_id
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/trequestdetail`, { params: payload } )

        let converted_data = convertTrainingRequestDates(data)
        
        return converted_data
    },

    async getTrainingRequestsById(trequest_id) {
        let payload = {
            'trequest_id': trequest_id
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/trequestsfilterbyid`, { params: payload } )
        
        let converted_data = convertTrainingRequestDates(data)
        
        return converted_data
    },

    async getTrainingRequestsByRequestType(substring) {
        let payload = {
            'search': substring
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/trequestsfilterbytype`, { params: payload } )
        
        let converted_data = convertTrainingRequestDates(data)
        
        return converted_data
    },

    async getTrainingRequestsByUser(substring) {
        let payload = {
            'substring': substring
        }
        const { data } = await request.get(`${Vue.prototype.$Config.backend}/rapi/v1/trequestsfilterbyuser`, { params: payload } )
        
        console.log("got: " + data[0].id + "   " + data[0].date)
        let converted_data = convertTrainingRequestDates(data)
        console.log("got: " + converted_data[0].id + "   " + converted_data[0].date)
        
        return converted_data
    },
}