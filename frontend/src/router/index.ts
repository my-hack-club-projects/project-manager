import { createRouter, createWebHistory } from 'vue-router'
// @ts-ignore
import LandingPageLayout from '../layouts/LandingPageLayout.vue'
// @ts-ignore
import ProjectManagerLayout from '../layouts/ProjectManagerLayout.vue'
// @ts-ignore
import HomeView from '../views/HomeView.vue'
// @ts-ignore

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
        // @ts-ignore
        { path: 'about', component: () => import('../views/AboutView.vue') },
        // @ts-ignore
        { path: 'contact', component: () => import('../views/ContactView.vue') },

        // @ts-ignore
        { path: 'logintest', component: () => import('../views/LoginTest.vue')},
        // Other routes that should be displayed in the LandingPageLayout
      ]
    },

    // Project manager routes
    {
      path: '/projects/',
      name: 'projects',
      component: ProjectManagerLayout,
      children: [
        // @ts-ignore
        { path: '', component: () => import('../views/ProjectListView.vue') },
        // @ts-ignore
        { path: 'analytics', component: () => import('../views/ProjectAnalytics.vue')},
        // @ts-ignore
        { path: 'view/:id(\\d+)', component: () => import('../views/ProjectView.vue') },
        
        // Other routes that should be displayed in the ProjectManagerLayout
      ]
    },
  ]
})

export default router
