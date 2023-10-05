import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import User from './views/User.vue'
import Users from './views/Users.vue'
import Projects from './views/Projects.vue'
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
            path: '/user',
            name: 'My account',
            component: User
        },          
        {
            path: '/users',
            name: 'Users',
            component: Users
        },             
        {
            path: '/projects',
            name: 'Projects',
            component: Projects
        }, 
        { path: '*', redirect: '/home' }  
    ]
})
