import { createRouter, createWebHistory } from 'vue-router'
import LandingPageLayout from '../layouts/LandingPageLayout.vue'
import ProjectManagerLayout from '../layouts/ProjectManagerLayout.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Landing page + user portfolio routes
    {
      path: '/',
      name: 'home',
      component: LandingPageLayout,
      children: [
        { path: '', component: HomeView },
        { path: 'about', component: () => import('../views/AboutView.vue') },
        { path: 'contact', component: () => import('../views/ContactView.vue') },

        { path: 'logintest', component: () => import('../views/LoginTest.vue')},
      ]
    },

    // Project manager routes
    {
      path: '/projects/',
      name: 'projects',
      component: ProjectManagerLayout,
      children: [
        { path: '', component: () => import('../views/ProjectListView.vue') },
        { path: 'analytics', component: () => import('../views/ProjectAnalytics.vue')},
        { path: 'view/:id(\\d+)', component: () => import('../views/ProjectView.vue') },
      ]
    },
  ]
})

export default router
