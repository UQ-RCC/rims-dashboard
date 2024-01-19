import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Projects from './views/Projects.vue'
import TrainingRequests from './views/TrainingRequests.vue'
//import User from './views/User.vue'
//import Projects from './views/Projects.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },                  
        {
            path: '/projects',
            name: 'Projects',
            component: Projects
        },
        {
            path: '/trainingrequests',
            name: 'Training Requests',
            component: TrainingRequests
        },         
        { path: '*', redirect: '/home' }  
    ]
})
