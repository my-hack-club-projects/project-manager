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

        { path: 'logintest', component: () => import('../views/LoginTest.vue') },

        { path: 'login', component: () => import('../views/LoginView.vue') },
        { path: 'register', component: () => import('../views/RegisterView.vue') },
        { path: 'email_sent', component: () => import('../views/PleaseConfirmEmail.vue') },
        { path: 'email_confirmed', component: () => import('../views/EmailConfirmed.vue') },
        { path: 'email_not_confirmed', component: () => import('../views/EmailNotConfirmed.vue') },
      ]
    },

    // Project manager routes
    {
      path: '/projects/',
      name: 'projects',
      component: ProjectManagerLayout,
      children: [
        { path: '', component: () => import('../views/ProjectListView.vue') },
        { path: 'analytics', component: () => import('../views/ProjectAnalytics.vue') },
        { path: ':categoryId(\\d+)/:projectId(\\d+)/view', component: () => import('../views/ProjectView.vue') },
      ]
    },
  ]
})

export default router
