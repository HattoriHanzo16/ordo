import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import RecordingsPage from '../components/RecordingsPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/recordings',
    name: 'Recordings',
    component: RecordingsPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 