import axios from 'axios'
import Vue from 'vue'

const service = axios.create({
    // baseURL: '', // url = base url + request url
    // withCredentials: true, // send cookies when cross-domain requests
    timeout: 100000 // request timeout
  })
  
  // request interceptor
  service.interceptors.request.use(
    config => {
      //Vue.$log.debug('Request intercepted')
      //if token is good
      if (Vue.prototype.$keycloak && Vue.prototype.$keycloak.token 
            && !Vue.prototype.$keycloak.isTokenExpired(Vue.prototype.$Config.keycloak.minValidity)) {
        //Vue.$log.debug('Token good, adding bearer')
        config.headers['Authorization'] = 'Bearer ' + Vue.prototype.$keycloak.token;
        return config
      }
      // elif token expired
      else if (Vue.prototype.$keycloak.isTokenExpired(Vue.prototype.$Config.keycloak.minValidity)) {

        Vue.prototype.$keycloak.updateToken(Vue.prototype.$Config.keycloak.minValidity).then(function(refreshed) {
          if (refreshed) {
            Vue.$log.info('Token refreshed' + refreshed)
            config.headers['Authorization'] = 'Bearer ' + Vue.prototype.$keycloak.token
            return config
          } else {
            Vue.$log.info('Token not refreshed, valid for '
              + Math.round(Vue.prototype.$keycloak.tokenParsed.exp + Vue.prototype.$keycloak.timeSkew - new Date().getTime() / 1000) + ' seconds')
          }
        }).catch(function() {
            Vue.$log.error(">>> Cannot refresh token")
            window.location.reload()
        })
      }
    },
    error => {
      // do something with request error
     // Vue.$log.error("request error here >>>>>>>>>>>>>>>>>>>>>>>>>>");
      //Vue.$log.error(error);
      return Promise.reject(error);
    }
  )

  
  // response interceptor
service.interceptors.response.use(
    /**
     * If you want to get http information such as headers or status
     * Please return  response => response
    */
  
    /**
     * Determine the request status by custom code
     * Here is just an example
     * You can also judge the status by HTTP Status Code
     */
    response => {
      return response
    },
    error => {
      //Vue.$log.error("response error here >>>>>>>>>>>>>>>>>>>>>>>>>>");
      //Vue.$log.error(error)
      // if token expired, refresh the whole page
      if(error.response.status === 401) {
        Vue.notify({
          group: 'sysnotif',
          type: 'warning',
          title: 'Authentication failure',
          text: String(error) + '<br/>Try refreshing the window, or check your credentials.<br/>'
        })
        //window.location.reload()
      } else {
        // Vue.notify({
        //   group: 'sysnotif',
        //   type: 'error',
        //   title: 'Error',
        //   text: 'There has been a problem:' + String(error)
        // })
      }
      return Promise.reject(error)
    }
  )
  
  export default service
