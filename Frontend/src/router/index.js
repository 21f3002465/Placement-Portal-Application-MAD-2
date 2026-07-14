import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminView from '../components/AdminView.vue'
import StudentView from '../components/StudentView.vue'
import CompanyView from '../components/CompanyView.vue'
import HomeView from '@/views/HomeView.vue'
import DashboardView from '@/views/DashboardView.vue'
import RegisterCompanyView from '@/views/RegisterCompanyView.vue'
import RegisterStudentView from '@/views/RegisterStudentView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/register/company',
      name:'RegisterCompany',
      component: RegisterCompanyView,
    },
     {
      path:'/register/student',
      name:'RegisterStudent',
      component: RegisterStudentView,
    },
      {
      path:'/',
      name:'Home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
    },
     {
      path:'/dashboard',
      name:'Dashboard',
      component: DashboardView,
    }
    // {
    //   path: '/admin',
    //   name: 'Admin',
    //   component: AdminView
    // },
    // {
    //   path:'/company',
    //   name:'Company',
    //   component: CompanyView
    // },
    // {
    //   path:'/student',
    //   name:'Student',
    //   component:StudentView
    // }
  ],
})

export default router
