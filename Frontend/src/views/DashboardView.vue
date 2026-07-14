<script setup>
import { ref, onMounted} from 'vue';
import { useRouter } from 'vue-router';

import AdminView from '../components/AdminView.vue';
import CompanyView from '../components/CompanyView.vue';
import StudentView from '../components/StudentView.vue';

// import router from '@/router/index.js';

const router = useRouter()
const UserRole = ref('')

onMounted(() => {
    // 1-Get user's role and token saved during login
    const saved_role=sessionStorage.getItem('UserRole')
    const saved_token=sessionStorage.getItem('token')

    // 2-if no such role or token exist, they are not logged in. They are kicked back to login page 
    if(!saved_role || !saved_token){
        router.push('/login')
        return
    }
    // 3- Update the reactive variable to activate the correct v-if layout
    UserRole.value = saved_role
})
const isLoggedIn = ref(false)

onMounted(() => {checkLoginstatus()})

function checkLoginstatus(){
  // If token is still there in, then user is logged out
  isLoggedIn.value = !!sessionStorage.getItem('token')
}

async function handleAuth() {
   if (isLoggedIn.value){
     const token = sessionStorage.getItem('token')
     await fetch('http://127.0.0.1:5000/api/Logout', {
            method:'POST',
            headers: {'Content-Type':'application/json',  'Authentication-Token': token },
     })
     sessionStorage.removeItem('token')
     sessionStorage.removeItem('UserRole')
     isLoggedIn.value = false
   }else
     router.push('/login')
    //  Redirecting to the Login page
  }


  // Enable search for serching users

</script>

<template>
  <!-- Common navifation bar for all  -->
<div class="card">
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <h3 class="text-center"> Welcome {{ UserRole }}</h3>
      </div>
     <div class="col-auto text-end">
        <form class="d-flex">
          <input class="form-control me-4" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>

    </div>
    </div>
  </div>
    <div class="container">
        <h1>
      <button class='btn btn-danger position-absolute top-0 end-0 m-3' @click="handleAuth" :class="isLoggedIn? 'btn-logout':'btn:login'">
        Logout
        </button>
    </h1>
    </div>

  <div>
    <!-- Components based on user's role -->
     <AdminView v-if="UserRole==='admin'"/>
     <CompanyView v-if="UserRole==='company'"/>
     <StudentView v-if="UserRole==='student'"/>
    </div>
  </div>
</template>