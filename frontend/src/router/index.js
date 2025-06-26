import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import RecordingsPage from '../components/RecordingsPage.vue'
import RecordingDetailPage from '../components/RecordingDetailPage.vue'
import SettingsPage from '../components/SettingsPage.vue'

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
  },
  {
    path: '/recordings/:id',
    name: 'RecordingDetail',
    component: RecordingDetailPage
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 