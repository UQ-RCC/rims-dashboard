import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Users from './views/Users.vue'
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
            path: '/users',
            name: 'Users',
            component: Users
        },             
        //User
        //Projects
        { path: '*', redirect: '/home' }  
    ]
})
